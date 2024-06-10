import dataclasses
import numbers
from dataclasses import field
from typing import Any, Dict, List, Optional

import mlflow.models
import pandas as pd

from databricks.rag_eval import constants, env_vars, schemas
from databricks.rag_eval.config import constants as config_constants
from databricks.rag_eval.config import example_config
from databricks.rag_eval.utils import collection_utils, enum_utils, error_utils

_ALLOWED_VARIABLES = [
    config_constants.ALLOWED_PROMPT_VARIABLE__REQUEST,
    config_constants.ALLOWED_PROMPT_VARIABLE__RESPONSE,
    config_constants.ALLOWED_PROMPT_VARIABLE__CONTEXT,
    config_constants.ALLOWED_PROMPT_VARIABLE__EXPECTED_RESPONSE,
]

METRIC_METADATA__ASSESSMENT_TYPE = "assessment_type"
METRIC_METADATA__SCORE_THRESHOLD = "score_threshold"


@dataclasses.dataclass(frozen=True)
class RateLimitConfig:
    """
    Rate limit configuration for the RAG evaluation harness.
    """

    quota: float
    """
    The number of tasks allowed to run in the time window.
    """

    time_window_in_seconds: float
    """
    The time window in seconds.
    """


@dataclasses.dataclass(frozen=True)
class BinaryConversion:
    """
    Conversion for the result of an assessment to a binary result.
    """

    threshold: float
    """
    Threshold value for converting to the binary.
    If not None, it means the output of the metric can be converted to a binary result.
    """
    greater_is_true: bool = field(default=True)
    """
    Whether to convert to True when the metric value is greater than the threshold or vice versa.
    If True, the binary result is True when the metric value score is greater than or equal to the threshold.
    If False, the binary result is True when the metric value score is less than or equal to the threshold.
    """

    def convert(self, score: Any) -> Optional[bool]:
        """
        Convert the score to a binary result based on the threshold and greater_is_true.

        If the score is not a real number, return None.
        """
        if isinstance(score, numbers.Real):
            # noinspection PyTypeChecker
            return (
                score >= self.threshold
                if self.greater_is_true
                else score <= self.threshold
            )
        else:
            return None

    def convert_to_score(self, rating: example_config.ExampleRating) -> str:
        """
        Convert an example rating to a score based on the threshold and greater_is_true.
        """
        return (
            "5"
            if self.greater_is_true == (rating == example_config.ExampleRating.YES)
            else "1"
        )


class AssessmentType(enum_utils.StrEnum):
    """Type of the assessment."""

    RETRIEVAL = "RETRIEVAL"
    """Assessment for retrieval. This is used to assess the quality of retrieval."""
    ANSWER = "ANSWER"
    """Assessment for answer. This is used to assess the quality of answer."""


@dataclasses.dataclass(frozen=True)
class AssessmentConfig:
    assessment_name: str

    assessment_type: AssessmentType

    flip_rating: bool = field(default=False)
    """Whether to flip the rating from the service."""

    # TODO(ML-40164): clean these bools into an array of required columns
    require_question: bool = field(default=False)
    """Whether the assessment requires input to be present in the dataset to eval."""

    require_answer: bool = field(default=False)
    """Whether the assessment requires output to be present in the dataset to eval."""

    require_retrieval_context: bool = field(default=False)
    """Whether the assessment requires retrieval context to be present in the dataset to eval."""

    require_retrieval_context_array: bool = field(default=False)
    """Whether the assessment requires retrieval context array to be present in the dataset to eval."""

    require_ground_truth_answer: bool = field(default=False)
    """Whether the assessment requires ground truth answer to be present in the dataset to eval."""

    require_ground_truth_retrieval_context: bool = field(default=False)
    """Whether the assessment requires ground truth retrieval to be present in the dataset to eval."""


@dataclasses.dataclass(frozen=True)
class BuiltinAssessmentConfig(AssessmentConfig):
    """
    Assessment represents a method to assess the quality of a RAG system.

    The method is defined by an MLflow EvaluationMetric object.
    """

    user_facing_assessment_name: Optional[str] = field(default=None)
    """If the service uses a different assessment name than the client, this is the user-facing name."""

    examples: List[example_config.AssessmentExample] = dataclasses.field(
        default_factory=list
    )

    domain_instructions: Optional[str] = field(default=None)
    """
    Domain-specific instruction to insert into the prompt for this assessment.
    """

    def __hash__(self):
        """
        Allow this object to be used as a key in a dictionary.
        """
        return hash(self.assessment_name)


@dataclasses.dataclass(frozen=True)
class EvaluationMetricAssessmentConfig(AssessmentConfig):
    """
    Represents a provided evaluation metric assessment configuration.

    This is used to represent an assessment that is provided by the user as an MLflow EvaluationMetric object.
    """

    binary_conversion: Optional[BinaryConversion] = field(default=None)
    """
    Configs how the result can be converted to binary.
    None if the result is not for converting to binary.
    """

    evaluation_metric: mlflow.models.EvaluationMetric = field(default=None)

    @classmethod
    def from_eval_metric(cls, evaluation_metric: mlflow.models.EvaluationMetric):
        """
        Create a EvaluationMetricAssessmentConfig object from an MLflow EvaluationMetric object.
        """
        try:
            assessment_type = AssessmentType(
                evaluation_metric.metric_metadata.get(
                    METRIC_METADATA__ASSESSMENT_TYPE, ""
                ).upper()
            )
        except Exception:
            raise error_utils.ValidationError(
                f"Invalid assessment type in evaluation metric: {evaluation_metric.name}. Evaluation metric "
                f"must contain metric metadata with key 'assessment_type' and value 'RETRIEVAL' or 'ANSWER'."
            )

        threshold = evaluation_metric.metric_metadata.get(
            METRIC_METADATA__SCORE_THRESHOLD, 3
        )

        return cls(
            assessment_name=evaluation_metric.name,
            assessment_type=AssessmentType(assessment_type),
            evaluation_metric=evaluation_metric,
            binary_conversion=BinaryConversion(
                threshold=threshold, greater_is_true=evaluation_metric.greater_is_better
            ),
        )

    def __hash__(self):
        """
        Allow this object to be used as a key in a dictionary.
        """
        return hash(self.assessment_name)


def _get_col_names_in_example_df_for_assessment(
    assessment_conf: BuiltinAssessmentConfig,
) -> (str, str):
    """
    Get the rating and rationale column names for a given assessment in the examples
    DataFrame
    """
    if assessment_conf.assessment_type == AssessmentType.ANSWER:
        assessment_prefix = (
            schemas.LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX
            + assessment_conf.assessment_name
        )
        rating_col = (
            assessment_prefix + schemas.LLM_JUDGED_RESPONSE_METRIC_RATING_COL_SUFFIX
        )
        rationale_col = (
            assessment_prefix + schemas.LLM_JUDGED_RESPONSE_METRIC_RATIONALE_COL_SUFFIX
        )
    else:
        assessment_prefix = (
            schemas.LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX
            + assessment_conf.assessment_name
        )
        rating_col = (
            assessment_prefix + schemas.LLM_JUDGED_RETRIEVAL_METRIC_RATING_COL_SUFFIX
        )
        rationale_col = (
            assessment_prefix + schemas.LLM_JUDGED_RETRIEVAL_METRIC_RATIONALE_COL_SUFFIX
        )
    return rating_col, rationale_col


def _explode_examples_on_context_chunk_array(
    examples_list, rating_col, rationale_col, assessment_conf
):
    """
    Given a list of examples, explode the examples into one example per chunk for a given retrieval assessment,
    excluding cases where the context chunk is None or the chunk contains a None content.
    :param examples_list: List of examples in the form of pd.DataFrame record dicts
    :param rating_col: Name of the rating column for this assessment
    :param rationale_col: Name of the rationale column for this assessment
    :param assessment_conf: Config for this assessment
    """
    exploded_examples_list = []
    for example in examples_list:
        context_array = example[config_constants.ALLOWED_PROMPT_VARIABLE__CONTEXT]
        if len(context_array) != len(example[rating_col]) or len(context_array) != len(
            example[rationale_col]
        ):
            raise error_utils.ValidationError(
                f"Number of retrieved contexts, ratings, and rationales must match. "
                f"Got {len(context_array)} contexts, {len(example[rating_col])} ratings, "
                f"and {len(example[rationale_col])} rationales for assessment {assessment_conf.assessment_name}."
            )
        for i, context in enumerate(context_array):
            if context is None:
                continue
            content = context.get(schemas.CHUNK_CONTENT_COL, None)
            if content is None:
                continue
            new_example = dict(example)  # Copy example
            new_example[config_constants.ALLOWED_PROMPT_VARIABLE__CONTEXT] = content
            new_example[rating_col] = example[rating_col][i]
            new_example[rationale_col] = example[rationale_col][i]
            exploded_examples_list.append(new_example)

    return exploded_examples_list


def _get_examples_with_concatenated_context(examples_list):
    """
    Given a list of examples, return a list of examples where the context chunks for each example
    are concatenated into a single string. This excludes cases where the context chunk is None or the chunk
    contains a None content.
    """
    result = []
    for example in examples_list:
        context_array = example.get(config_constants.ALLOWED_PROMPT_VARIABLE__CONTEXT)
        if context_array:
            chunks = [
                context.get(schemas.CHUNK_CONTENT_COL, None)
                for context in context_array
                if context is not None
            ]
            context_str = constants.DEFAULT_CONTEXT_CONCATENATION_DELIMITER.join(
                [chunk for chunk in chunks if chunk is not None]
            )
            example[config_constants.ALLOWED_PROMPT_VARIABLE__CONTEXT] = context_str
        result.append(example)
    return result


def _get_example_configs_from_examples_df(
    examples_df: Optional[pd.DataFrame],
    assessment_conf: BuiltinAssessmentConfig,
) -> List[example_config.AssessmentExample]:
    """
    Given a DataFrame of examples in the same format as the mlflow.evaluate output df,
    return a list of AssessmentExample targeted at the given assessment config.
    """
    if examples_df is None:
        return []

    rating_col, rationale_col = _get_col_names_in_example_df_for_assessment(
        assessment_conf
    )

    if (
        rating_col not in examples_df.columns
        or rationale_col not in examples_df.columns
    ):
        return []

    cols_to_select = [
        config_constants.ALLOWED_PROMPT_VARIABLE__REQUEST,
        rating_col,
        rationale_col,
    ]

    if assessment_conf.require_answer:
        cols_to_select.append(config_constants.ALLOWED_PROMPT_VARIABLE__RESPONSE)
    if (
        assessment_conf.require_retrieval_context
        or assessment_conf.require_retrieval_context_array
    ):
        cols_to_select.append(config_constants.ALLOWED_PROMPT_VARIABLE__CONTEXT)
    if assessment_conf.require_ground_truth_answer:
        cols_to_select.append(
            config_constants.ALLOWED_PROMPT_VARIABLE__EXPECTED_RESPONSE
        )

    #  Exclude rows where any column is None except for rationale
    relevant_df = examples_df[cols_to_select]
    relevant_df = relevant_df.dropna(
        subset=relevant_df.columns.difference([rationale_col])
    )
    examples_list = relevant_df.to_dict(orient="records")

    if len(examples_list) > env_vars.RAG_EVAL_MAX_FEW_SHOT_EXAMPLES.get():
        raise error_utils.ValidationError(
            f"The number of rows in `examples_df` exceeds the maximum: {env_vars.RAG_EVAL_MAX_FEW_SHOT_EXAMPLES.get()}. "
            f"Got {len(examples_list)} rows. Please reduce the number of examples."
        )

    if assessment_conf.require_retrieval_context_array:
        # This is a retrieval metric. Need to return one example per chunk
        exploded_examples_list = _explode_examples_on_context_chunk_array(
            examples_list, rating_col, rationale_col, assessment_conf
        )
    elif assessment_conf.require_retrieval_context:
        # Answer metric. Return example with concatenated context string
        exploded_examples_list = _get_examples_with_concatenated_context(examples_list)
    else:
        exploded_examples_list = (
            examples_list  # Don't need to explode, context will not be used
        )

    if len(exploded_examples_list) > env_vars.RAG_EVAL_MAX_FEW_SHOT_EXAMPLES.get():
        raise error_utils.ValidationError(
            f"The total number of chunks in `examples_df` exceeds the maximum: {env_vars.RAG_EVAL_MAX_FEW_SHOT_EXAMPLES.get()}. "
            f"Got {len(exploded_examples_list)} chunks. Please reduce the number of rows or chunks per row."
        )

    return [
        example_config.AssessmentExample(
            variables=collection_utils.omit_keys(
                example,
                [
                    rating_col,
                    rationale_col,
                ],
            ),
            rating=example_config.ExampleRating(example.get(rating_col)),
            rationale=example.get(rationale_col),
        )
        for example in exploded_examples_list
    ]


def create_builtin_assessment_configs(
    assessment_list: List[str],
    examples_df: Optional[pd.DataFrame],
    domain_instructions: Optional[Dict[str, str]],
) -> List[BuiltinAssessmentConfig]:
    """
    Parse a list of builtin assessments (and optional examples) into a list of BuiltinAssessmentConfigs
    """
    from databricks.rag_eval.judges import builtin_judge

    assessment_configs = []
    if domain_instructions is None:
        domain_instructions = {}

    for assessment_name in assessment_list:
        builtin_assessment_conf = (
            builtin_judge.get_builtin_assessment_config_with_name_with_instruction(
                assessment_name, domain_instructions.get(assessment_name, None)
            )
        )

        df_examples = _get_example_configs_from_examples_df(
            examples_df, builtin_assessment_conf
        )
        builtin_assessment_conf = dataclasses.replace(
            builtin_assessment_conf, examples=df_examples
        )
        assessment_configs.append(builtin_assessment_conf)

    return assessment_configs


def create_custom_eval_metric_assessment_configs(
    eval_metrics: Optional[List[mlflow.models.EvaluationMetric]],
) -> List[EvaluationMetricAssessmentConfig]:
    """
    Create AssessmentJudge objects from a list of custom evaluation metrics.
    """
    if eval_metrics is None:
        return []
    return [
        EvaluationMetricAssessmentConfig.from_eval_metric(metric)
        for metric in eval_metrics
    ]
