"""Entities for evaluation."""

import dataclasses
import functools
import hashlib
from typing import Any, Collection, Dict, List, Mapping, Optional, TypeAlias, Union

import mlflow.entities as mlflow_entities
import pandas as pd

from databricks.rag_eval import constants, schemas
from databricks.rag_eval.config import assessment_config, example_config
from databricks.rag_eval.utils import (
    collection_utils,
    enum_utils,
    input_output_utils,
    serialization_utils,
)

ChunkInputData = Union[str, Dict[str, Any]]
RetrievalContextInputData = List[Optional[ChunkInputData]]


@dataclasses.dataclass
class Chunk:
    doc_uri: Optional[str] = None
    content: Optional[str] = None

    @classmethod
    def from_input_data(cls, input_data: Optional[ChunkInputData]) -> Optional["Chunk"]:
        """
        Construct a Chunk from a dictionary optionally containing doc_uri and content.

        An input chunk of a retrieval context can be:
          - A doc URI; or
          - A dictionary with the schema defined in schemas.CHUNK_SCHEMA
        """
        if input_output_utils.is_none_or_nan(input_data):
            return None
        if isinstance(input_data, str):
            return cls(doc_uri=input_data)
        else:
            return cls(
                doc_uri=input_data.get(schemas.DOC_URI_COL),
                content=input_data.get(schemas.CHUNK_CONTENT_COL),
            )


class RetrievalContext(List[Optional[Chunk]]):
    def __init__(self, chunks: Collection[Optional[Chunk]]):
        super().__init__(chunks)

    def concat_chunk_content(
        self, delimiter: str = constants.DEFAULT_CONTEXT_CONCATENATION_DELIMITER
    ) -> Optional[str]:
        """
        Concatenate the non-empty content of the chunks to a string with the given delimiter.
        Return None if all the contents are empty.
        """
        non_empty_contents = [
            chunk.content for chunk in self if chunk is not None and chunk.content
        ]
        return delimiter.join(non_empty_contents) if non_empty_contents else None

    def get_doc_uris(self) -> List[Optional[str]]:
        """Get the list of doc URIs in the retrieval context."""
        return [chunk.doc_uri for chunk in self if chunk is not None]

    def to_output_dict(self) -> List[Dict[str, str]]:
        """Convert the RetrievalContext to a list of dictionaries with the schema defined in schemas.CHUNK_SCHEMA."""
        return [
            (
                {
                    schemas.DOC_URI_COL: chunk.doc_uri,
                    schemas.CHUNK_CONTENT_COL: chunk.content,
                }
                if chunk is not None
                else None
            )
            for chunk in self
        ]

    @classmethod
    def from_input_data(
        cls, input_data: Optional[RetrievalContextInputData]
    ) -> Optional["RetrievalContext"]:
        """
        Construct a RetrievalContext from the input.

        Input can be:
        - A list of doc URIs
        - A list of dictionaries with the schema defined in schemas.CHUNK_SCHEMA
        """
        if input_output_utils.is_none_or_nan(input_data):
            return None
        return cls([Chunk.from_input_data(chunk_data) for chunk_data in input_data])


class CategoricalRating(enum_utils.StrEnum):
    """A categorical rating for an assessment."""

    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, value: str):
        value = value.lower()
        for member in cls:
            if member == value:
                return member
        return cls.UNKNOWN

    @classmethod
    def from_example_rating(
        cls, rating: example_config.ExampleRating
    ) -> "CategoricalRating":
        """Convert an ExampleRating to a CategoricalRating."""
        match rating:
            case example_config.ExampleRating.YES:
                return cls.YES
            case example_config.ExampleRating.NO:
                return cls.NO
            case _:
                return cls.UNKNOWN


@dataclasses.dataclass
class Rating:
    double_value: Optional[float]
    rationale: Optional[str]
    error_message: Optional[str]
    categorical_value: Optional[CategoricalRating]

    @classmethod
    def build(
        cls,
        *,
        rationale: str,
        double_value: Optional[float],
        categorical_value: Optional[CategoricalRating | str] = None,
    ) -> "Rating":
        """Build a normal Rating with a categorical value, a double value, and a rationale."""
        if categorical_value is not None and not isinstance(
            categorical_value, CategoricalRating
        ):
            categorical_value = CategoricalRating(categorical_value)
        return cls(
            double_value=double_value,
            rationale=rationale,
            categorical_value=categorical_value,
            error_message=None,
        )

    @classmethod
    def from_rationale(cls, rationale: str) -> "Rating":
        """Build a Rating with only a rationale."""
        return cls(
            double_value=None,
            rationale=rationale,
            categorical_value=None,
            error_message=None,
        )

    @classmethod
    def error(cls, error_message: str) -> "Rating":
        """Build an error Rating with an error message."""
        return cls(
            double_value=None,
            rationale=None,
            categorical_value=None,
            error_message=error_message,
        )

    @classmethod
    def flip(cls, rating: "Rating") -> "Rating":
        """Built a Rating with the inverse categorical and float values of the input Rating."""
        if rating.double_value is not None and (
            rating.double_value < 1.0 or rating.double_value > 5.0
        ):
            raise ValueError(
                f"Cannot flip the rating of double value: {rating.double_value}."
            )

        match rating.categorical_value:
            case CategoricalRating.YES:
                flipped_categorical_value = CategoricalRating.NO
                flipped_double_value = 1.0
            case CategoricalRating.NO:
                flipped_categorical_value = CategoricalRating.YES
                flipped_double_value = 5.0
            case CategoricalRating.UNKNOWN:
                flipped_categorical_value = CategoricalRating.UNKNOWN
                flipped_double_value = None
            case None:
                flipped_categorical_value = None
                flipped_double_value = None
            case _:
                raise ValueError(
                    f"Cannot flip the rating of categorical value: {rating.categorical_value}"
                )

        return cls(
            double_value=flipped_double_value,
            rationale=rating.rationale,
            categorical_value=flipped_categorical_value,
            error_message=rating.error_message,
        )


PositionalRating: TypeAlias = Mapping[int, Rating]
"""
A mapping from position to rating.
Position refers to the position of the chunk in the retrieval context.
It is used to represent the ratings of the chunks in the retrieval context.
"""


@functools.total_ordering
@dataclasses.dataclass
class EvalItem:
    """
    Represents a row in the evaluation dataset. It contains information needed to evaluate a question.
    """

    question_id: str
    """Unique identifier for the eval item."""

    question: str
    """String representation of the model input that is used for evaluation."""

    raw_request: Any
    """Passed as input to the model when `evaluate` is called with a model."""

    answer: Optional[str]
    """String representation of the model output that is used for evaluation."""

    retrieval_context: Optional[RetrievalContext]
    """Retrieval context that is used for evaluation."""

    ground_truth_answer: Optional[str]
    """String representation of the ground truth answer."""

    ground_truth_retrieval_context: Optional[RetrievalContext]
    """Ground truth retrieval context."""

    trace: Optional[mlflow_entities.Trace]
    """Trace of the model invocation."""

    model_error_message: Optional[str] = None
    """Error message if the model invocation fails."""

    @property
    def concatenated_retrieval_context(self) -> Optional[str]:
        """Get the concatenated content of the retrieval context.
        Return None if there is no non-empty retrieval context content."""
        return (
            self.retrieval_context.concat_chunk_content()
            if self.retrieval_context
            else None
        )

    @classmethod
    def from_pd_series(cls, series: pd.Series):
        """
        Create an EvalItem from a row of MLflow EvaluationDataset data.
        """
        retrieved_context = RetrievalContext.from_input_data(
            series.get(schemas.RETRIEVED_CONTEXT_COL)
        )

        expected_retrieved_context = RetrievalContext.from_input_data(
            series.get(schemas.EXPECTED_RETRIEVED_CONTEXT_COL)
        )

        question = input_output_utils.input_to_string(series[schemas.REQUEST_COL])
        question_id = series.get(schemas.REQUEST_ID_COL)
        if input_output_utils.is_none_or_nan(question_id):
            question_id = hashlib.sha256(question.encode()).hexdigest()
        answer = input_output_utils.output_to_string(series.get(schemas.RESPONSE_COL))
        ground_truth_answer = input_output_utils.output_to_string(
            series.get(schemas.EXPECTED_RESPONSE_COL)
        )
        trace = series.get(schemas.TRACE_COL)
        if input_output_utils.is_none_or_nan(trace):
            trace = None
        else:
            trace = serialization_utils.deserialize_trace(trace)

        return cls(
            question_id=question_id,
            question=question,
            raw_request=series.get(schemas.REQUEST_COL),
            answer=answer,
            retrieval_context=retrieved_context,
            ground_truth_answer=ground_truth_answer,
            ground_truth_retrieval_context=expected_retrieved_context,
            trace=trace,
        )

    def __eq__(self, other):
        if not hasattr(other, "question_id"):
            return NotImplemented
        return self.question_id == other.question_id

    def __lt__(self, other):
        if not hasattr(other, "question_id"):
            return NotImplemented
        return self.question_id < other.question_id


@dataclasses.dataclass
class AssessmentResult:
    """Holds the result of an assessment."""

    assessment_name: str
    assessment_type: assessment_config.AssessmentType


@dataclasses.dataclass
class AnswerAssessmentResult(AssessmentResult):
    """Holds the result of an answer assessment."""

    rating: Rating
    assessment_type: assessment_config.AssessmentType = dataclasses.field(
        init=False, default=assessment_config.AssessmentType.ANSWER
    )


@dataclasses.dataclass
class RetrievalAssessmentResult(AssessmentResult):
    """Holds the result of a retrieval assessment."""

    positional_rating: PositionalRating
    assessment_type: assessment_config.AssessmentType = dataclasses.field(
        init=False, default=assessment_config.AssessmentType.RETRIEVAL
    )


@dataclasses.dataclass
class AssessmentLog:
    """Holds the assessment logs for a single eval item."""

    eval_item: EvalItem
    assessment_results: Collection[AssessmentResult]
    """
    A collection of AssessmentResult.
    Assessment name is should be unique for each eval item.
    """

    def __post_init__(self):
        if not self.assessment_results:
            self.assessment_results = []


@dataclasses.dataclass
class EvalResult:
    """Holds the result of the evaluation for an eval item."""

    eval_item: EvalItem
    assessment_results: Collection[AssessmentResult]

    total_input_token_count: Optional[int]
    """Total input tokens across all spans in the trace."""
    total_output_token_count: Optional[int]
    """Total output tokens across all spans in the trace."""
    total_token_count: Optional[int]
    """Total tokens across all spans in the trace."""

    exact_match: Optional[bool]
    """Whether the response exactly matches the ground truth answer."""

    latency_seconds: Optional[float]
    """Latency of model invoking in seconds."""

    ground_truth_retrieval_metrics: Mapping[str, float]
    """
    Ground truth retrieval metrics, such as precision/recall, etc.
    It is computed by comparing the ground truth retrieval context with the retrieval context.

    metric_name -> score, e.g. {recall: 0.1}
    """

    llm_judged_retrieval_metrics: Mapping[str, float]
    """
    LLM-judged retrieval metrics.
    e.g. Use the "context_relevance" assessment result to calculate precision of the retrieval.

    metric_name -> score, e.g. {precision: 0.5}
    """

    ground_truth_document_ratings: Optional[List[CategoricalRating]]
    """
    Ground truth document ratings. Whether each document in the retrieval context is in the ground truth or not.
    """

    def to_pd_series(self) -> pd.Series:
        """Converts the EvalResult to a flattened pd.Series."""
        # Extracting relevant fields from eval_item and assessment_results
        inputs = {
            schemas.REQUEST_ID_COL: self.eval_item.question_id,
            schemas.REQUEST_COL: self.eval_item.question,
            schemas.RESPONSE_COL: self.eval_item.answer,
            schemas.EXPECTED_RETRIEVED_CONTEXT_COL: (
                self.eval_item.ground_truth_retrieval_context.to_output_dict()
                if self.eval_item.ground_truth_retrieval_context
                else None
            ),
            schemas.EXPECTED_RESPONSE_COL: self.eval_item.ground_truth_answer,
            schemas.RETRIEVED_CONTEXT_COL: (
                self.eval_item.retrieval_context.to_output_dict()
                if self.eval_item.retrieval_context
                else None
            ),
            schemas.TRACE_COL: serialization_utils.serialize_trace(
                self.eval_item.trace
            ),
        }
        if self.eval_item.model_error_message:
            inputs[schemas.MODEL_ERROR_MESSAGE_COL] = self.eval_item.model_error_message

        # Flatten the assessment results into the series
        assessments: Dict[str, schemas.ASSESSMENT_RESULT_TYPE] = {}
        for assessment in self.assessment_results:
            if isinstance(assessment, AnswerAssessmentResult):
                if assessment.rating.categorical_value is not None:
                    assessments[
                        schemas.get_response_llm_rating_col_name(
                            assessment.assessment_name
                        )
                    ] = assessment.rating.categorical_value
                if assessment.rating.rationale is not None:
                    assessments[
                        schemas.get_response_llm_rationale_col_name(
                            assessment.assessment_name
                        )
                    ] = assessment.rating.rationale
                if assessment.rating.error_message is not None:
                    assessments[
                        schemas.get_response_llm_error_message_col_name(
                            assessment.assessment_name
                        )
                    ] = assessment.rating.error_message
            elif isinstance(assessment, RetrievalAssessmentResult):
                # Convert the positional_rating to a list of ratings ordered by position
                # For missing positions, use an error rating. This should not happen in practice.
                ratings_ordered_by_position: List[Rating] = (
                    collection_utils.position_map_to_list(
                        assessment.positional_rating,
                        default=Rating.error("Missing rating"),
                    )
                )
                if any(
                    rating.categorical_value is not None
                    for rating in ratings_ordered_by_position
                ):
                    assessments[
                        schemas.get_retrieval_llm_rating_col_name(
                            assessment.assessment_name
                        )
                    ] = [
                        rating.categorical_value
                        for rating in ratings_ordered_by_position
                    ]
                if any(
                    rating.rationale is not None
                    for rating in ratings_ordered_by_position
                ):
                    assessments[
                        schemas.get_retrieval_llm_rationale_col_name(
                            assessment.assessment_name
                        )
                    ] = [rating.rationale for rating in ratings_ordered_by_position]
                if any(
                    rating.error_message is not None
                    for rating in ratings_ordered_by_position
                ):
                    assessments[
                        schemas.get_retrieval_llm_error_message_col_name(
                            assessment.assessment_name
                        )
                    ] = [rating.error_message for rating in ratings_ordered_by_position]

        metrics: Dict[str, schemas.METRIC_RESULT_TYPE] = {
            **{
                f"{schemas.LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX}{metric_name}": metric_value
                for metric_name, metric_value in self.llm_judged_retrieval_metrics.items()
            },
            **{
                f"{schemas.GROUND_TRUTH_RETRIEVAL_METRIC_COL_PREFIX}{metric_name}": metric_value
                for metric_name, metric_value in self.ground_truth_retrieval_metrics.items()
            },
            schemas.GROUND_TRUTH_DOCUMENT_RATING_COL: self.ground_truth_document_ratings,
            schemas.TOTAL_INPUT_TOKEN_COUNT_COL: self.total_input_token_count,
            schemas.TOTAL_OUTPUT_TOKEN_COUNT_COL: self.total_output_token_count,
            schemas.TOTAL_TOKEN_COUNT_COL: self.total_token_count,
            schemas.LATENCY_SECONDS_COL: self.latency_seconds,
        }
        # Remove None values in metrics
        metrics = {key: value for key, value in metrics.items() if value is not None}

        # Merge dictionaries and convert to pd.Series
        combined_data = {**inputs, **assessments, **metrics}
        return pd.Series(combined_data)
