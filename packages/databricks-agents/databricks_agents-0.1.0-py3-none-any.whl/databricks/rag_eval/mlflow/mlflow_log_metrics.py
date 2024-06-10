"""Generate the metrics logged into MLflow."""

import collections
from typing import Dict, List, Mapping, Optional

import numpy as np

from databricks.rag_eval import schemas
from databricks.rag_eval.evaluation import entities
from databricks.rag_eval.judges import builtin_judge
from databricks.rag_eval.utils import rating_utils

_AVERAGE_SUFFIX = "/average"
_PERCENTAGE_SUFFIX = "/percentage"


def generate_mlflow_metrics(
    eval_results: List[entities.EvalResult],
) -> Dict[str, float]:
    """
    Generates per-run MLflow metrics.

    :param eval_results: List of EvalResult objects
    :return: Dictionary of aggregated MLflow metrics
    """

    result = {
        **{
            f"{schemas.GROUND_TRUTH_RETRIEVAL_METRIC_COL_PREFIX}{metric_name}{_AVERAGE_SUFFIX}": metric_value
            for metric_name, metric_value in _compute_avg_for_metric_group(
                eval_results, "ground_truth_retrieval_metrics"
            ).items()
        },
        **{
            f"{schemas.LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX}{metric_name}{_AVERAGE_SUFFIX}": metric_value
            for metric_name, metric_value in _compute_avg_for_metric_group(
                eval_results, "llm_judged_retrieval_metrics"
            ).items()
        },
        **{
            f"{schemas.LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX}{assessment_name}"
            f"{schemas.LLM_JUDGED_RESPONSE_METRIC_RATING_COL_SUFFIX}{_PERCENTAGE_SUFFIX}": true_rate
            for assessment_name, true_rate in _compute_true_rate_answer_assessment(
                eval_results
            ).items()
        },
    }

    # Other generation avg metrics
    for metric_name in [
        "total_input_token_count",
        "total_output_token_count",
        "total_token_count",
        "latency_seconds",
    ]:
        metric_value = _compute_avg_for_metric(eval_results, metric_name)
        if metric_value is not None:
            result[f"agent/{metric_name}{_AVERAGE_SUFFIX}"] = metric_value

    # Count error in judges
    for assessment_name, error_count in _count_error_in_judges(eval_results).items():
        result[f"judge/{assessment_name}/error_count"] = error_count

    return result


def _compute_avg_for_metric_group(
    eval_results: List[entities.EvalResult],
    metric_group_name: str,
) -> Dict[str, float]:
    """
    Compute the average a group of metrics across all eval results.
    The metric group is expected to be a Mapping[str, float] in each EvalResult.

    :param eval_results: List of EvalResult objects
    :param metric_group_name: Name of the metric group
    :return: Dictionary of average value for each metric in the group
    """
    metric_value_sums = collections.defaultdict(float)
    metric_value_counts = collections.defaultdict(int)
    for eval_result in eval_results:
        metric_group: Mapping[str, float] = getattr(eval_result, metric_group_name, {})
        for (
            metric_name,
            metric_value,
        ) in metric_group.items():
            metric_name = builtin_judge.translate_to_eval_assessment_name(metric_name)
            metric_value_sums[metric_name] += metric_value
            metric_value_counts[metric_name] += 1
    return {
        metric_name: metric_value_sums[metric_name] / metric_value_counts[metric_name]
        for metric_name in metric_value_sums
        if metric_value_counts[metric_name] > 0
    }


def _compute_avg_for_metric(
    eval_results: List[entities.EvalResult], metric_name: str
) -> Optional[float]:
    """
    Compute the average of a metric across all eval results.

    Returns None if the metric is not present in any of the eval results.

    :param eval_results: List of EvalResult objects
    :param metric_name: Name of the metric
    :return: Average of the metric
    """
    metric_values = [
        getattr(eval_result, metric_name, None)
        for eval_result in eval_results
        if getattr(eval_result, metric_name, None) is not None
    ]

    return np.average(metric_values) if metric_values else None


def _count_true_for_metric(
    eval_results: List[entities.EvalResult], metric_name: str
) -> int:
    """
    Count the number of `True` of a metric across all eval results.

    :param eval_results: List of EvalResult objects
    :param metric_name: Name of the metric
    :return: Count of the metric
    """
    return np.count_nonzero(
        [getattr(eval_result, metric_name, None) for eval_result in eval_results]
    )


def _compute_true_rate_answer_assessment(
    eval_results: List[entities.EvalResult],
) -> Dict[str, float]:
    """
    Compute the rate of `True` in the answer assessment results.

    rate of `True` = count of `True` / count of non-null values.

    :param eval_results: List of EvalResult objects
    :return: Dictionary of rate of `True` for each answer assessment
    """
    true_counts = collections.defaultdict(int)
    non_null_counts = collections.defaultdict(int)
    for eval_result in eval_results:
        for assessment_result in eval_result.assessment_results:
            if isinstance(assessment_result, entities.AnswerAssessmentResult):
                true_counts[assessment_result.assessment_name] += (
                    assessment_result.rating.categorical_value
                    == entities.CategoricalRating.YES
                )
                non_null_counts[assessment_result.assessment_name] += (
                    assessment_result.rating.categorical_value is not None
                )

    return {
        assessment_name: true_counts[assessment_name] / non_null_counts[assessment_name]
        for assessment_name in true_counts
        if non_null_counts[assessment_name] > 0
    }


def _count_error_in_judges(
    eval_results: List[entities.EvalResult],
) -> Dict[str, int]:
    """
    Count the number of errors in the assessment results.

    :param eval_results: List of EvalResult objects
    :return: Dictionary of count of errors for each assessment
    """
    error_counts = collections.defaultdict(int)
    for eval_result in eval_results:
        for assessment_result in eval_result.assessment_results:
            if isinstance(assessment_result, entities.AnswerAssessmentResult):
                if _is_real_error_rating(assessment_result.rating):
                    error_counts[assessment_result.assessment_name] += 1
            elif isinstance(assessment_result, entities.RetrievalAssessmentResult):
                for positional_rating in assessment_result.positional_rating.values():
                    if _is_real_error_rating(positional_rating):
                        error_counts[assessment_result.assessment_name] += 1

    return error_counts


def _is_real_error_rating(rate: entities.Rating) -> bool:
    """Check if the rate is a real error. Missing input error is not considered as a real error."""
    return rate.error_message is not None and not rating_utils.is_missing_input_error(
        rate.error_message
    )
