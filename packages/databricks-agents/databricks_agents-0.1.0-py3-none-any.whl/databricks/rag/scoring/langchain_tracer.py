import threading
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from langchain_core.tracers.base import BaseTracer
from langchain_core.tracers.schemas import Run
from typing_extensions import override

import databricks.rag.scoring.predictions as rag_predictions
from databricks.rag import constants
from databricks.rag.scoring.schema_v2 import (
    MLFLOW_TRACE_SCHEMA_VERSION,
    Event,
    Span,
    SpanContext,
    SpanType,
    StatusCode,
)

MLFLOW_SPAN_INPUTS_KEY = "mlflow.spanInputs"
MLFLOW_SPAN_OUTPUTS_KEY = "mlflow.spanOutputs"
MLFLOW_SPAN_TYPE_KEY = "mlflow.spanType"

COMPONENT_SPAN_TYPE_MAPPING = {
    "llm": SpanType.LLM,
    "retriever": SpanType.RETRIEVER,
    "tool": SpanType.TOOL,
    "agent": SpanType.AGENT,
    "chat_model": SpanType.LLM,
    "chain": SpanType.CHAIN,
}


# Duplicate the predictions.Chunk class to
# avoid circular imports
@dataclass
class Chunk:
    chunk_id: Optional[str] = None
    doc_uri: Optional[str] = None
    content: Optional[str] = None


def convert_lc_run_events_to_span_events(
    lc_run_events: List[Dict[str, Any]],
) -> List[Event]:
    results = []
    for i, lc_run_event in enumerate(lc_run_events):
        event_time = lc_run_event.pop("time", None) or lc_run_event.pop(
            "timestamp", None
        )
        if event_time:
            name = lc_run_event.pop("name", None) or f"event_{i}"
            if isinstance(event_time, datetime):
                event_time = convert_datetime_to_nanoseconds(event_time)
            elif not isinstance(event_time, int):
                # skip the conversion of this event
                continue
            results.append(
                Event(
                    name=name,
                    timestamp=event_time,
                    attributes=lc_run_event,
                )
            )
    return results


def lc_retriever_outputs_convert_func(
    outputs: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """
    Convert Retriever outputs format from
    {
        "documents": [
            Document(page_content="...", metadata={...}, type="Document"),
            ...
        ]
    }
    to
    {
        "chunks": [
            {
                "chunk_id": "...",
                "doc_uri": "...",
                "content": "...",
            },
            ...
        ]
    }
    """
    from langchain_core.documents import Document

    if outputs is None:
        return None

    chunk_id_col = getattr(
        rag_predictions,
        "__databricks_vector_search_primary_key__",
        constants.VS_INDEX_ID_COL,
    )
    doc_uri_col = getattr(
        rag_predictions,
        "__databricks_vector_search_doc_uri__",
        constants.VS_INDEX_DOC_URL_COL,
    )
    return {
        "chunks": [
            asdict(
                Chunk(
                    chunk_id=doc.metadata.get(chunk_id_col),
                    doc_uri=doc.metadata.get(doc_uri_col),
                    content=doc.page_content,
                )
            )
            for doc in outputs.get("documents", [])
            if isinstance(doc, Document)
        ]
    }


def lc_llm_inputs_convert_func(
    inputs: Optional[Dict[str, List[str]]],
) -> Optional[Dict[str, str]]:
    """
    Convert LLM inputs format from
    {"prompts": ["prompt1"...]}
    to
    {"prompt": "prompt1"}
    # TODO: multiple prompts is not supported for now
    """
    if inputs is None:
        return None
    prompts = inputs.get("prompts", [])
    if len(prompts) == 0:
        prompt = ""
    elif len(prompts) == 1:
        prompt = prompts[0]
    else:
        raise NotImplementedError(f"Multiple prompts not supported yet. Got: {prompts}")
    return {"prompt": prompt}


def lc_llm_outputs_convert_func(
    outputs: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """
    Convert LLM outputs format from
    {
        # generations is List[List[Generation]] because
        # each input could have multiple candidate generations.
        "generations": [[{"text": "...", "generation_info": {...}, "type": "Generation"}]],
        "llm_output": {...},
        "run": [{"run_id": "..."}],
    }
    to
    {
        # Convert to str by extracting first text field of Generation
        # TODO: This assumes we are not in batch situation where we have multiple generations per input
        "generated_text": "generated_text1",
    }
    """
    if outputs is None:
        return None
    generated_text: str = ""
    if "generations" in outputs:
        generations: List[List[Dict[str, Any]]] = outputs["generations"]
        if len(generations) > 0 and len(generations[0]) > 0:
            first_generation: Dict[str, Any] = generations[0][0]
            generated_text = first_generation.get("text", "")
    return {"generated_text": generated_text}


def convert_datetime_to_nanoseconds(timestamp: Optional[datetime]):
    if timestamp is None:
        return
    if isinstance(timestamp, datetime):
        return int(timestamp.timestamp() * 1e9)
    raise TypeError(f"Expecting timestamp to be datetime, got {type(timestamp)}")


def convert_nanoseconds_to_datetime(timestamp: Optional[int]):
    if timestamp is None:
        return
    if isinstance(timestamp, int):
        return datetime.fromtimestamp(timestamp / 1e9)
    raise TypeError(f"Expecting timestamp to be int, got {type(timestamp)}")


def _convert_lc_run_to_span(
    run: Run,
    status_code: StatusCode,
    status_message="",
    span_type=None,
    input_convert_func=None,
    output_convert_func=None,
) -> Span:
    if callable(output_convert_func):
        outputs = output_convert_func(run.outputs)
    else:
        outputs = run.outputs
    if callable(input_convert_func):
        inputs = input_convert_func(run.inputs)
    else:
        inputs = run.inputs
    if span_type is None:
        span_type = COMPONENT_SPAN_TYPE_MAPPING.get(run.run_type, SpanType.UNKNOWN)
    if run.parent_run_id is not None:
        parent_span_id = str(run.parent_run_id)
    else:
        parent_span_id = None
    attributes = run.extra
    attributes.update(
        {
            MLFLOW_SPAN_INPUTS_KEY: inputs,
            MLFLOW_SPAN_OUTPUTS_KEY: outputs,
            MLFLOW_SPAN_TYPE_KEY: str(span_type),
        }
    )
    return Span(
        name=run.name,
        context=SpanContext(span_id=str(run.id)),
        parent_id=parent_span_id,
        start_time=convert_datetime_to_nanoseconds(run.start_time),
        end_time=convert_datetime_to_nanoseconds(run.end_time),
        status_code=status_code,
        status_message=status_message,
        attributes=attributes,
        events=convert_lc_run_events_to_span_events(deepcopy(run.events)),
    )


class DatabricksLangChainTracer(BaseTracer):
    """
    Callback to inject to LangChain to trace the execution of the model.

    Args:
        convert_inputs_outputs: Whether to convert the outputs of the components.
                         This is for backwards compatibility of old Trace schema. If set to True,
                         default functions for converting LLM and Retrieval outputs to old schema
                         will be applied.

    Example inputs and outputs for different components:
        llm
            - inputs: {"prompts": prompts}
            - outputs:
                - if convert_inputs_outputs is False (LLMResult.dict())
                    {
                        "generations": [{"text": "...", "generation_info": {...}, "type": "Generation"}], # This includes generation_text
                        "llm_output": {...},
                        "run": [{"run_id": "..."}],
                    }
                - if convert_inputs_outputs is True
                    {"generations": [["generated_text1", "generated_text2"], ["generated_text3"...]]}
        retriever
            - inputs: {"query": query}
            - outputs:
                - if convert_inputs_outputs is False
                    {"documents": [
                        "page_content": "...",
                        "metadata": {...}, # This includes chunk_id and doc_uri
                        "type": "Document",
                    ]}
                - if convert_inputs_outputs is True
                    {"chunks": [{"chunk_id": "...", "doc_uri": "...", "content": "...",}]}

    trace is a dictionary with the following keys:
        - spans: List of Span objects
        - start_time: Start time of the trace
        - end_time: End time of the trace
    """

    def __init__(self, convert_inputs_outputs: bool = False):
        super().__init__()
        self.convert_inputs_outputs = convert_inputs_outputs
        self.trace = None
        self._span_buffer: Dict[str, Span] = {}
        self._lock = threading.Lock()

    @override
    def _persist_run(self, run: Run) -> None:
        """
        Persist the run to the trace.
        Only invoke once because this run has no parent run.
        Initialize the trace and update it at the end of the run.
        """
        self.trace = {MLFLOW_TRACE_SCHEMA_VERSION: 2}

    def _convert_span_and_flush(
        self,
        run: Run,
        status_code: StatusCode,
        status_message="",
        span_type=None,
    ) -> None:
        """
        Convert the run to a span and flush it to the span buffer.
        If the run is the root run, update the trace with the span buffer.
        """
        input_convert_func = None
        output_convert_func = None
        if self.convert_inputs_outputs:
            if COMPONENT_SPAN_TYPE_MAPPING.get(run.run_type) == SpanType.LLM:
                input_convert_func = lc_llm_inputs_convert_func
                output_convert_func = lc_llm_outputs_convert_func
            elif COMPONENT_SPAN_TYPE_MAPPING.get(run.run_type) == SpanType.RETRIEVER:
                output_convert_func = lc_retriever_outputs_convert_func

        # multiple components can run in parallel and invoke this method
        # at the same time. We add a lock here to make the tracer thread safe.
        with self._lock:
            span = _convert_lc_run_to_span(
                run,
                status_code,
                status_message,
                span_type,
                input_convert_func,
                output_convert_func,
            )
            self._span_buffer[str(run.id)] = span
        # current span is the root span
        if self.trace is not None:
            # Preserve the correct order of spans sorting by start_time ASC
            self.trace["spans"] = sorted(
                self._span_buffer.values(), key=lambda span: span.start_time
            )
            # Save trace start/end_timestamp as datetime, so when it converts to json
            # it can be saved as isoformat, further compatible with TimestampType in table schema
            self.trace["start_timestamp"] = convert_nanoseconds_to_datetime(
                self._span_buffer[str(run.id)].start_time
            )
            self.trace["end_timestamp"] = convert_nanoseconds_to_datetime(
                self._span_buffer[str(run.id)].end_time
            )

    @override
    def _on_run_create(self, run: Run) -> None:
        """
        Process a run upon creation.
        This is invoked inside _start_trace for each on_*_start method.
        We convert the run to a span and flush it to the span buffer in case
        any exception is raised before on_*_end or on_*_error is invoked.
        """
        if str(run.id) in self._span_buffer:
            raise Exception(
                f"Internal Error: _on_run_create called twice for the same run {run.id}"
            )
        self._convert_span_and_flush(
            run=run, status_code=StatusCode.ERROR, status_message="Span not completed"
        )

    @override
    def _on_llm_end(self, run: Run) -> None:
        """Process the LLM Run."""
        if str(run.id) not in self._span_buffer:
            raise Exception("Internal Error: on_llm_end called without on_llm_start")
        self._convert_span_and_flush(
            run=run,
            status_code=StatusCode.OK,
        )

    @override
    def _on_llm_error(self, run: Run) -> None:
        """Process the LLM Run upon error."""
        if str(run.id) not in self._span_buffer:
            raise Exception("Internal Error: on_llm_error called without on_llm_start")
        self._convert_span_and_flush(
            run=run,
            status_code=StatusCode.ERROR,
            status_message=run.error,
        )

    @override
    def _on_retriever_end(self, run: Run) -> None:
        """Process the Retriever Run."""
        if str(run.id) not in self._span_buffer:
            raise Exception(
                "Internal Error: on_retriever_end called without on_retriever_start"
            )
        self._convert_span_and_flush(
            run=run,
            status_code=StatusCode.OK,
        )

    @override
    def _on_retriever_error(self, run: Run) -> None:
        """Process the Retriever Run upon error."""
        if str(run.id) not in self._span_buffer:
            raise Exception(
                "Internal Error: on_retriever_error called without on_retriever_start"
            )
        self._convert_span_and_flush(
            run=run, status_code=StatusCode.ERROR, status_message=run.error
        )

    @override
    def _on_chain_end(self, run: Run) -> None:
        """Process the Chain Run."""
        if str(run.id) not in self._span_buffer:
            raise Exception(
                "Internal Error: on_chain_end called without on_chain_start"
            )
        self._convert_span_and_flush(
            run=run, status_code=StatusCode.OK, span_type=SpanType.CHAIN
        )

    @override
    def _on_chain_error(self, run: Run) -> None:
        """Process the Chain Run upon error."""
        if str(run.id) not in self._span_buffer:
            raise Exception(
                "Internal Error: on_chain_error called without on_chain_start"
            )
        self._convert_span_and_flush(
            run=run,
            status_code=StatusCode.ERROR,
            status_message=run.error,
            span_type=SpanType.CHAIN,
        )

    @override
    def _on_tool_end(self, run: Run) -> None:
        """Process the Tool Run."""
        if str(run.id) not in self._span_buffer:
            raise Exception("Internal Error: on_tool_end called without on_tool_start")
        self._convert_span_and_flush(run=run, status_code=StatusCode.OK)

    @override
    def _on_tool_error(self, run: Run) -> None:
        """Process the Tool Run upon error."""
        if str(run.id) not in self._span_buffer:
            raise Exception(
                "Internal Error: on_tool_error called without on_tool_start"
            )
        self._convert_span_and_flush(
            run=run, status_code=StatusCode.ERROR, status_message=run.error
        )
