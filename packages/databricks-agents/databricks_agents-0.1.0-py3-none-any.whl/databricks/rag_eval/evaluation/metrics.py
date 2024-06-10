import logging
from typing import Collection, List, Mapping, Optional

import mlflow
import pandas as pd

from databricks.rag_eval import constants, schemas
from databricks.rag_eval.evaluation import entities, traces

_logger = logging.getLogger(__name__)


def compute_eval_metrics(
    assessment_log: entities.AssessmentLog,
) -> entities.EvalResult:
    """
    Compute the per-eval-item metrics and produce the eval result.

    The aggregation is performed on the per-eval-item granularity – for each eval-item in the input eval dataset,
    this function produces an EvalResult.
    """
    eval_item = assessment_log.eval_item
    trace_token_count = traces.compute_total_token_count(eval_item.trace)

    return entities.EvalResult(
        eval_item=eval_item,
        assessment_results=assessment_log.assessment_results,
        total_input_token_count=trace_token_count.input_token_count,
        total_output_token_count=trace_token_count.output_token_count,
        total_token_count=trace_token_count.total_token_count,
        exact_match=_compute_exact_match(eval_item),
        latency_seconds=_compute_latency_seconds(eval_item),
        ground_truth_retrieval_metrics=_compute_ground_truth_retrieval_metrics(
            eval_item
        ),
        llm_judged_retrieval_metrics=_compute_llm_judged_retrieval_metrics(
            assessment_log.assessment_results
        ),
        ground_truth_document_ratings=_compute_ground_truth_document_ratings(eval_item),
    )


# ================ Latency ================
def _compute_latency_seconds(eval_item: entities.EvalItem) -> Optional[float]:
    """Compute the latency (in fractional seconds to a microsecond granularity) from the trace information."""
    if (
        eval_item.trace is None
        or eval_item.trace.info is None
        or eval_item.trace.info.execution_time_ms is None
    ):
        return None
    else:
        return eval_item.trace.info.execution_time_ms / 1000.0


# ================ Exact Match ================
def _compute_exact_match(
    eval_item: entities.EvalItem,
) -> Optional[bool]:
    """Compute the exact match. The answer is considered an exact match if it is equal to the ground truth answer."""
    if eval_item.answer is None or eval_item.ground_truth_answer is None:
        return None
    return eval_item.answer.strip() == eval_item.ground_truth_answer.strip()


# ================ Ground Truth Retrieval Metrics ================
def _compute_ground_truth_retrieval_metrics(
    eval_item: entities.EvalItem,
) -> Mapping[str, float]:
    """
    Compute the ground truth retrieval metrics.

    The ground truth retrieval metrics include: precision, recall, etc.

    The metrics is calculated based on the doc_uri of retrieval context and ground truth retrieval context
    in the eval item.

    The method outputs the following metrics:
    - The recall for the whole context (K = length of retrieval)
    """
    if not eval_item.retrieval_context or not eval_item.ground_truth_retrieval_context:
        return {}
    retrieved_docs = eval_item.retrieval_context.get_doc_uris()
    ground_truth_docs = eval_item.ground_truth_retrieval_context.get_doc_uris()
    if not retrieved_docs or not ground_truth_docs:
        return {}

    results = {}
    k = len(retrieved_docs)
    for metric_name in constants.GROUND_TRUTH_RETRIEVAL_METRIC_NAMES:
        mlflow_eval_metric = getattr(mlflow.metrics, f"{metric_name}_at_k")(k)

        eval_fn = mlflow_eval_metric.eval_fn
        try:
            metric_value = eval_fn(
                pd.Series([retrieved_docs]), pd.Series([ground_truth_docs])
            )
            score = metric_value.scores[0]
            results[f"{schemas.GROUND_TRUTH_DOCUMENT_PREFIX}{metric_name}"] = score
        except Exception as e:
            full_metric_name = (
                schemas.GROUND_TRUTH_RETRIEVAL_METRIC_COL_PREFIX
                + schemas.GROUND_TRUTH_DOCUMENT_PREFIX
                + metric_name
            )
            _logger.debug(
                f"Error in computing {full_metric_name} for eval_item {eval_item}: {e}"
            )

    return results


# ================ Ground Truth Document Ratings ================
def _compute_ground_truth_document_ratings(
    eval_item: entities.EvalItem,
) -> Optional[List[entities.CategoricalRating]]:
    """
    Compute the ground truth retrieved document ratings.

    The ratings are calculated based on the doc_uri of retrieval context and ground truth retrieval context.
    For each document in the retrieval context, we rate it Yes if it is in the ground truth retrieval context,
    and No otherwise.

    Return None if the retrieval context or ground truth retrieval context is None.
    """
    if not eval_item.retrieval_context or not eval_item.ground_truth_retrieval_context:
        return None
    retrieved_docs = eval_item.retrieval_context.get_doc_uris()
    ground_truth_docs = eval_item.ground_truth_retrieval_context.get_doc_uris()
    if not retrieved_docs or not ground_truth_docs:
        return None

    return [
        (
            (
                entities.CategoricalRating.YES
                if retrieved_doc in ground_truth_docs
                else entities.CategoricalRating.NO
            )
            if retrieved_doc is not None
            else None
        )
        for retrieved_doc in retrieved_docs
    ]


# ================ LLM Judged Retrieval Metrics ================
def _compute_llm_judged_retrieval_metrics(
    assessment_results: Collection[entities.AssessmentResult],
) -> Mapping[str, float]:
    """
    Compute the LLM-judged precision metrics using the results of the retrieval assessment.

    We use the positional_rating of the retrieval assessment results to compute the precision at k metrics.
    """
    results = {}
    for assessment_result in assessment_results:
        if not isinstance(assessment_result, entities.RetrievalAssessmentResult):
            continue
        ratings = [
            rating
            for _, rating in assessment_result.positional_rating.items()
            if rating.categorical_value is not None
        ]
        if not ratings:
            continue
        precision = sum(
            r.categorical_value == entities.CategoricalRating.YES for r in ratings
        ) / len(ratings)
        results[f"{assessment_result.assessment_name}/precision"] = precision
    return results
