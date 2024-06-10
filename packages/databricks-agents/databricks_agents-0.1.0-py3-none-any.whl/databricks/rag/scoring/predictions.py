import os
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence
from uuid import UUID

from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.documents import Document
from langchain_core.outputs import LLMResult
from mlflow.langchain import _LangChainModelWrapper

import databricks
from databricks.rag import constants
from databricks.rag.scoring.langchain_tracer import DatabricksLangChainTracer
from databricks.rag.scoring.schema_v2 import Span

def _rag_trace_v2_enabled():
    return os.environ.get("RAG_TRACE_V2_ENABLED", "false").lower() == "true"

# Note: This function needs to be where here so it can be accessed in the prediction module easily.
# The code below adds the schema as global variables to the module so that it can be accessed
# during tracing and in the review UI.
def set_vector_search_schema(
    primary_key: str,
    text_column: Optional[str] = "",
    doc_uri: Optional[str] = "",
    other_columns: Optional[List[str]] = None,
):
    """
    After defining your vector store in a Python file or notebook, call
    set_vector_search_schema() so that we can correctly map the vector index
    columns. These columns would be used during tracing and in the review UI.

    :param primary_key: The primary key of the vector index.
    :param text_column: The name of the text column to use for the embeddings.
    :param doc_uri: The name of the column that contains the document URI.
    :param other_columns: A list of other columns that are part of the vector index
                          that need to be retrieved during trace logging.

    Note: Make sure the text column specified is in the index.

    Example:
    ```
    from databricks.rag import set_vector_search_schema

    set_vector_search_schema(
        primary_key="chunk_id",
        text_column="chunk_text",
        doc_uri="doc_uri",
        other_columns=["title"],
    )
    """
    globals()["__databricks_vector_search_primary_key__"] = primary_key
    globals()["__databricks_vector_search_text_column__"] = text_column
    globals()["__databricks_vector_search_doc_uri__"] = doc_uri
    globals()["__databricks_vector_search_other_columns__"] = (
        other_columns if other_columns is not None else []
    )


@dataclass
class Error:
    type: Optional[str] = None
    message: Optional[str] = None


@dataclass
class TextGeneration:
    prompt: Optional[str] = None
    generated_text: Optional[str] = None


@dataclass
class Chunk:
    chunk_id: Optional[str] = None
    doc_uri: Optional[str] = None
    content: Optional[str] = None


@dataclass
class Retrieval:
    query_text: Optional[str] = None
    chunks: Optional[List[Chunk]] = None


@dataclass
class TraceStep:
    step_id: Optional[str] = field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = None
    type: Optional[str] = None
    start_timestamp: Optional[datetime] = None
    end_timestamp: Optional[datetime] = None
    retrieval: Optional[Retrieval] = None
    text_generation: Optional[TextGeneration] = None

    def __post_init__(self):
        provided_fields = [
            self.retrieval is not None,
            self.text_generation is not None,
        ]
        if sum(provided_fields) != 1:
            raise ValueError(
                "Exactly one of llm_output or retriever_output must be provided."
            )

    def to_json(self) -> str:
        data = asdict(self)
        # Convert datetime fields to string for JSON serialization
        data["start_timestamp"] = data["start_timestamp"].isoformat()
        data["end_timestamp"] = data["end_timestamp"].isoformat()
        return json.dumps(data)


@dataclass
class Trace:
    steps: Optional[List[TraceStep]] = None
    start_timestamp: Optional[datetime] = None
    end_timestamp: Optional[datetime] = None
    steps: Optional[List[TraceStep]] = None
    is_truncated: Optional[bool] = False

    def to_json_obj(self):
        data = asdict(self)
        for step in data["steps"]:
            if step["start_timestamp"] is not None:
                step["start_timestamp"] = step["start_timestamp"].isoformat()
            if step["end_timestamp"] is not None:
                step["end_timestamp"] = step["end_timestamp"].isoformat()

        # Convert datetime fields to string for JSON serialization
        if data["start_timestamp"] is not None:
            data["start_timestamp"] = data["start_timestamp"].isoformat()
        if data["end_timestamp"] is not None:
            data["end_timestamp"] = data["end_timestamp"].isoformat()
        return data


class DatabricksChainCallback(BaseCallbackHandler):
    def __init__(self, verbose=False):
        super().__init__()
        self.verbose = verbose
        self._name_counts: Dict[str, int] = {}
        self._trace: Optional[TraceStep] = None
        self.trace_buffer = []

    def _flush_trace(self):
        # generate unique name
        self._trace.name = self._generate_unique_name(self._trace.name)
        self.trace_buffer.append(self._trace)
        self._trace = None

    def _generate_unique_name(self, name: str) -> str:
        # update the name count
        if name in self._name_counts:
            self._name_counts[name] = self._name_counts[name] + 1
        else:
            self._name_counts[name] = 1
        unique_name = name
        if name in self._name_counts:
            idx = self._name_counts[name]
            unique_name += f"_{str(idx)}"
        return unique_name

    def _consistency_check(self, step_name):
        # get current trace name
        current_trace = self._trace

        if step_name in ["on_llm_start", "on_retriever_start"]:
            # ensure that there is no active trace
            if current_trace is not None:
                raise Exception(
                    f"Internal Error: {step_name} called without on_*_end or on_*_error"
                )
        elif step_name in ["on_llm_end", "on_llm_error"]:
            # ensure that there is an active trace
            if current_trace is None:
                raise Exception(
                    f"Internal Error: {step_name} called without on_llm_start"
                )
            # ensure that the active trace is an LLM trace
            if current_trace.type != "LLM_GENERATION":
                raise Exception(
                    f"Internal Error: {step_name} called without active LLM trace"
                )
        elif step_name in ["on_retriever_end", "on_retriever_error"]:
            # ensure that there is an active trace
            if current_trace is None:
                raise Exception(
                    f"Internal Error: {step_name} called without on_retriever_start"
                )
            # ensure that the active trace is a retrieval trace
            if current_trace.type != "RETRIEVAL":
                raise Exception(
                    f"Internal Error: {step_name} called without active retrieval trace"
                )

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        **kwargs: Any,
    ) -> Any:
        self._consistency_check("on_llm_start")
        cur_time = datetime.now()
        if len(prompts) == 0:
            prompt = ""
        elif len(prompts) == 1:
            prompt = prompts[0]
        else:
            # TODO(Avesh): When is len(prompts) > 1?
            raise NotImplementedError("Multiple prompts not supported yet.")

        self._trace = TraceStep(
            name="generation",
            type="LLM_GENERATION",
            start_timestamp=cur_time,
            text_generation=TextGeneration(prompt=prompt),
        )

    def on_llm_end(
        self,
        response: LLMResult,
        **kwargs: Any,
    ) -> Any:
        self._consistency_check("on_llm_end")
        cur_time = datetime.now()
        if response and hasattr(response, "generations") and response.generations:
            if len(response.generations) > 0 and len(response.generations[0]) > 0:
                # TODO(Avesh): Can we have len(response.generations)>1?
                if hasattr(response.generations[0][0], "text"):
                    generated_text = response.generations[0][0].text
                else:
                    generated_text = ""
            else:
                generated_text = ""
        else:
            generated_text = ""

        self._trace.text_generation.generated_text = generated_text
        self._trace.end_timestamp = cur_time
        self._flush_trace()

    def on_llm_error(
        self,
        error: BaseException,
        **kwargs: Any,
    ) -> Any:
        self._consistency_check("on_llm_error")
        cur_time = datetime.now()
        self._trace.end_timestamp = cur_time
        self._flush_trace()

    def on_retriever_start(
        self,
        serialized: Dict[str, Any],
        query: str,
        **kwargs: Any,
    ) -> Any:
        self._consistency_check("on_retriever_start")
        cur_time = datetime.now()
        self._trace = TraceStep(
            name="retrieval",
            type="RETRIEVAL",
            start_timestamp=cur_time,
            retrieval=Retrieval(query_text=query),
        )

    def on_retriever_end(
        self,
        documents: Sequence[Document],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        self._consistency_check("on_retriever_end")

        cur_time = datetime.now()
        # edit the self.retrieval object to include the list of Chunks
        chunk_id_col = getattr(
            databricks.rag.scoring.predictions,
            "__databricks_vector_search_primary_key__",
            constants.VS_INDEX_ID_COL,
        )
        doc_uri_col = getattr(
            databricks.rag.scoring.predictions,
            "__databricks_vector_search_doc_uri__",
            constants.VS_INDEX_DOC_URL_COL,
        )
        chunks = [
            Chunk(
                chunk_id=doc.metadata.get(chunk_id_col),
                doc_uri=doc.metadata.get(doc_uri_col),
                content=doc.page_content,
            )
            for doc in documents
        ]
        self._trace.retrieval.chunks = chunks
        self._trace.end_timestamp = cur_time
        self._flush_trace()

    def on_retriever_error(self, error: BaseException, **kwargs: Any) -> Any:
        self._consistency_check("on_retriever_error")
        cur_time = datetime.now()
        self._trace.end_timestamp = cur_time
        self._flush_trace()


def _default_converter(o):
    if isinstance(o, Trace):
        return o.to_json_obj()
    if isinstance(o, Span):
        return o.json()
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


# The API specification is subject to change
class RAGCallback:
    def _convert_trace_buffer_to_trace_object(self, trace_buffer):
        if len(trace_buffer) == 0:
            start_timestamp = None
            end_timestamp = None
        elif len(trace_buffer) == 1:
            start_timestamp = trace_buffer[0].start_timestamp
            end_timestamp = trace_buffer[0].end_timestamp
        else:
            start_timestamp = trace_buffer[0].start_timestamp
            end_timestamp = trace_buffer[-1].end_timestamp
        return Trace(
            steps=trace_buffer,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )

    def _dump_callback_trace(self, callback):
        if isinstance(callback, DatabricksChainCallback):
            return json.dumps(
                self._convert_trace_buffer_to_trace_object(callback.trace_buffer),
                default=_default_converter,
            )
        if isinstance(callback, DatabricksLangChainTracer):
            return json.dumps(
                callback.trace,
                default=_default_converter,
            )

    def invoke(self, langchain_model, input):
        if _rag_trace_v2_enabled():
            handler = DatabricksLangChainTracer(convert_inputs_outputs=True)
        else:
            handler = DatabricksChainCallback()
        try:
            langchain_wrapped_model = _LangChainModelWrapper(langchain_model)
            response = langchain_wrapped_model._predict_with_callbacks(
                input, callback_handlers=[handler], convert_chat_responses=True
            )
        except Exception as e:
            print(
                f"WARNING: LangChain invocation failed with {type(e).__name__}: {str(e)}"
            )
            trace_json_string = self._dump_callback_trace(handler)
            return (None, trace_json_string)

        trace_json_string = self._dump_callback_trace(handler)
        return (response, trace_json_string)
