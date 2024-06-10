import abc
import dataclasses
import logging
import numbers
from concurrent.futures import ThreadPoolExecutor, as_completed
from inspect import signature
from typing import Any, List, Optional

import pandas as pd
from mlflow import MlflowException
from mlflow.deployments import set_deployments_target
from mlflow.metrics import MetricValue
from mlflow.models import EvaluationMetric

from databricks.rag_eval import constants
from databricks.rag_eval.clients.llmjudge import llm_judge_client
from databricks.rag_eval.config import (
    assessment_config,
)
from databricks.rag_eval.config import constants as config_constants
from databricks.rag_eval.evaluation import entities
from databricks.rag_eval.judges import constants as judge_constants
from databricks.rag_eval.utils import error_utils, rate_limit

_logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class Assessment(abc.ABC):
    """
    Assessment represents a method to assess the quality of a RAG system.
    """

    @abc.abstractmethod
    def run(self, eval_item: entities.EvalItem) -> List[entities.AssessmentResult]:
        """
        Run the assessment on a single eval item and produce a list of assessment results.
        A single eval item can produce multiple assessment results since multiple assessments can be batch computed
        together for a single EvalItem.

        If the eval item does not have required fields for the assessment, return an empty list.

        :param eval_item: The eval item to assess.
        :return: A list of assessment results.
        """
        pass


@dataclasses.dataclass(frozen=True)
class BuiltInAssessment(Assessment):
    """
    Builtin assessment using the LLM judge service to compute the assessments
    """

    config: assessment_config.BuiltinAssessmentConfig
    """Configuration for the assessment."""
    rate_limiter: rate_limit.RateLimiter
    """Rate limiter to apply to the LLM endpoint caller."""
    llm_judge_client: llm_judge_client.LlmJudgeClient
    """LLM judge client to use for the assessment."""

    def run(self, eval_item: entities.EvalItem) -> List[entities.AssessmentResult]:
        with self.rate_limiter:
            result = self.llm_judge_client.get_assessment(
                eval_item,
                self.config.assessment_name,
                self.config.assessment_type,
                self.config.examples,
                self.config.domain_instructions,
            )
            return result


@dataclasses.dataclass(frozen=True)
class EvaluationMetricAssessment(Assessment):
    """
    Custom assessment using the MLflow EvaluationMetric provided by the user.
    """

    config: assessment_config.EvaluationMetricAssessmentConfig
    """Configuration for the assessment."""
    rate_limiter: rate_limit.RateLimiter
    """Rate limiter to apply to the eval_fn calls."""
    llm_judge_client: llm_judge_client.LlmJudgeClient
    """LLM judge client to use to emit usage data."""

    @property
    def name(self):
        return self.config.assessment_name

    @property
    def assessment_type(self):
        return self.config.assessment_type

    def run(self, eval_item: entities.EvalItem) -> List[entities.AssessmentResult]:
        # Note: this lets us call the Databricks endpoints.
        set_deployments_target("databricks")
        try:
            self.llm_judge_client.emit_chat_assessment_usage_event(self.config)
        except Exception:  # pylint: disable=broad-except
            # Don't want to indicate to users that we're emitting data
            pass

        match self.assessment_type:
            case assessment_config.AssessmentType.RETRIEVAL:
                return [self._run_retrieval_assessment(eval_item)]
            case assessment_config.AssessmentType.ANSWER:
                return [self._run_answer_assessment(eval_item)]
            case _:
                raise error_utils.ValidationError(
                    f"Assessment type '{self.assessment_type}' is not supported."
                    f"Supported types are: {assessment_config.AssessmentType.ANSWER} and {assessment_config.AssessmentType.RETRIEVAL}."
                )

    def _run_answer_assessment(
        self, eval_item: entities.EvalItem
    ) -> entities.AnswerAssessmentResult:
        """
        Run the answer assessment on the eval item and produce an answer assessment result.
        """
        eval_metric = self._load_metric()
        with self.rate_limiter:
            rating: entities.Rating = self._compute_rating(
                eval_metric, eval_item, chunk=None, pos=None
            )

        return entities.AnswerAssessmentResult(
            assessment_name=self.name,
            rating=rating,
        )

    def _run_retrieval_assessment(
        self, eval_item: entities.EvalItem
    ) -> entities.RetrievalAssessmentResult:
        """
        Run the retrieval assessment on the eval item and produce a retrieval assessment result.

        The retrieval assessment is a positional assessment, where each position in the retrieval context
        is rated separately.
        """
        positional_ratings = {}
        eval_metric = self._load_metric()
        for pos, chunk in enumerate(eval_item.retrieval_context):
            # Skip the chunk if it is empty
            if chunk is None or not chunk.content:
                positional_ratings[pos] = entities.Rating.from_rationale(
                    constants.CHUNK_CONTENT_IS_EMPTY_RATIONALE,
                )
                continue

            rating: entities.Rating = self._compute_rating(
                eval_metric, eval_item, chunk, pos
            )

            positional_ratings[pos] = rating

        return entities.RetrievalAssessmentResult(
            assessment_name=self.name,
            positional_rating=positional_ratings,
        )

    def _load_metric(self) -> EvaluationMetric:
        """
        Loads the Mlflow EvaluationMetric object.
        """
        return self.config.evaluation_metric

    def _get_eval_fn_params(self) -> List[str]:
        """
        Get a list of parameter names needed for the eval_fn of the metric.
        """
        eval_metric = self._load_metric()
        return list(signature(eval_metric.eval_fn).parameters.keys())

    def _compute_rating(
        self,
        eval_metric: EvaluationMetric,
        eval_item: entities.EvalItem,
        chunk: Optional[entities.Chunk],
        pos: Optional[int],
    ) -> entities.Rating:
        """
        Compute a Rating for an assessment given the EvalItem, input chunk and position.
        If chunk and position are both defined, treat this as a retrieval assessment.
        """
        eval_fn_input_params = self._get_eval_fn_params()
        try:
            if "kwargs" in eval_fn_input_params:
                # Pass in eval items directly
                eval_fn_kwargs = _extract_mlflow_eval_fn_kwargs(eval_item, chunk)
                with self.rate_limiter:
                    metric_value = eval_metric.eval_fn(**eval_fn_kwargs)
            else:
                # Assuming "retrieved_content" is from the chunk content for each chunk in the retrieval context
                # and other params are extracted from eval_item
                eval_fn_args = [
                    (
                        pd.Series([chunk.content])
                        if param == judge_constants.RETRIEVED_CONTENT
                        and chunk is not None
                        and pos is not None
                        else pd.Series([_extract_mlflow_eval_fn_args(eval_item, param)])
                    )
                    for param in eval_fn_input_params
                ]
                # Rate limit the request to the built-in assessment LLM judge model
                with self.rate_limiter:
                    metric_value = eval_metric.eval_fn(*eval_fn_args)
        except MlflowException as e:
            # Can happen if the eval item doesn't contain the required fields
            # for the custom metric. We can't determine this beforehand as the
            # prompt is baked into the eval_fn and can't be extracted.
            # In this case, return an error Rating
            return entities.Rating.error(str(e))

        return _mlflow_eval_value_to_rating(metric_value, self.config.binary_conversion)


def generate_llm_assessments(
    *, eval_item: entities.EvalItem, assessments: List[Assessment]
) -> entities.AssessmentLog:
    """
    Performs the LLM judged assessment on a EvalItems and generates a AssessmentLog
    using the given LLM judge model and assessments.

    The method only uses the compatible assessments for the given eval dataset.
    An assessment is incompatible if it requires extra information which is missing in the eval item.
    For example, an assessment is not compatible if it requires retrieval context
    but the eval dataset does not have retrieval context.

    :param eval_item: The eval item to evaluate on.
    :param assessments: The list of assessments to use.
    """
    if not assessments:
        return entities.AssessmentLog(eval_item=eval_item, assessment_results=[])

    assessment_results: List[entities.AssessmentResult] = []
    # Use a thread pool to run assessments in parallel
    # Use the number of assessments as the number of workers
    with ThreadPoolExecutor(max_workers=len(assessments)) as executor:
        futures = [
            executor.submit(
                _run_assessment,
                eval_item=eval_item,
                assessment=assessment,
            )
            for assessment in assessments
        ]

        try:
            for future in as_completed(futures):
                result = future.result()
                assessment_results.extend(result)
        except KeyboardInterrupt:
            for future in futures:
                future.cancel()
            print("Assessment generation interrupted.")
            raise

    return entities.AssessmentLog(
        eval_item=eval_item,
        assessment_results=assessment_results,
    )


def _run_assessment(
    eval_item: entities.EvalItem,
    assessment: Assessment,
) -> List[entities.AssessmentResult]:
    """
    Run the assessment on a single eval item and produce a list of assessment results.
    """
    return assessment.run(eval_item)


def _extract_mlflow_eval_fn_args(eval_item: entities.EvalItem, param: str) -> Any:
    """
    Extract the value of eval_fn arguments from the eval item given the param name.

    Param name should be in sync with the signature of the eval_fn in MLflow.
    """
    match param:
        case judge_constants.MLFLOW_EVAL_FN_INPUTS:
            return eval_item.question
        case judge_constants.MLFLOW_EVAL_FN_METRICS:
            return ""
        case judge_constants.MLFLOW_EVAL_FN_PREDICTIONS:
            return eval_item.answer
        case judge_constants.MLFLOW_EVAL_FN_CONTEXT:
            return eval_item.concatenated_retrieval_context
        case judge_constants.MLFLOW_EVAL_FN_TARGETS:
            return eval_item.ground_truth_answer


def _extract_mlflow_eval_fn_kwargs(
    eval_item: entities.EvalItem, chunk: Optional[entities.Chunk]
) -> Any:
    """
    Given an eval_item, create the dictionary of kwargs to provide to the eval_fn for a custom
    metric. Excludes None values.
    """
    base_kwargs = {
        config_constants.ALLOWED_PROMPT_VARIABLE__REQUEST: eval_item.question,
        config_constants.ALLOWED_PROMPT_VARIABLE__RESPONSE: eval_item.answer,
        config_constants.ALLOWED_PROMPT_VARIABLE__CONTEXT: (
            eval_item.concatenated_retrieval_context if chunk is None else chunk.content
        ),
        config_constants.ALLOWED_PROMPT_VARIABLE__EXPECTED_RESPONSE: eval_item.ground_truth_answer,
    }
    return {
        key: pd.Series([value])
        for key, value in base_kwargs.items()
        if value is not None
    }


def _mlflow_eval_value_to_rating(
    mlflow_metric_value: Optional[MetricValue],
    binary_conversion: Optional[assessment_config.BinaryConversion],
) -> entities.Rating:
    """
    Convert the MLflow metric value to a Rating object.
    Assumes that the MLflow metric value only contains results for a single row.
    """
    # Return error rating if the scores or justifications are empty
    if (
        mlflow_metric_value is None
        or mlflow_metric_value.scores is None
        or len(mlflow_metric_value.scores) == 0
        or mlflow_metric_value.justifications is None
        or len(mlflow_metric_value.justifications) == 0
    ):
        return entities.Rating.error(
            f"Fail to get the assessment result: {mlflow_metric_value}"
        )

    # Assume that the scores and justifications are for a single row
    assert (
        len(mlflow_metric_value.scores) == 1
    ), f"Expected a single score, but got {len(mlflow_metric_value.scores)} scores."
    score = mlflow_metric_value.scores[0]
    justification = mlflow_metric_value.justifications[0]

    if score is None:
        # If the score is None, it means there is as an error.
        # In this case, the error message is the justification.
        return entities.Rating.error(justification)

    if not isinstance(score, numbers.Real):
        # If the score is not a real number, we treat it as an error.
        return entities.Rating.error(
            f"Could not extract numerical score from '{score}': {justification}"
        )
    else:
        bool_value = binary_conversion.convert(score) if binary_conversion else None
        categorical_value = (
            entities.CategoricalRating.YES
            if bool_value
            else (entities.CategoricalRating.NO if bool_value is not None else None)
        )
        return entities.Rating.build(
            categorical_value=categorical_value,
            double_value=float(score),
            rationale=justification,
        )
