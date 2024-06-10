"""Entry point to the evaluation harness"""

from __future__ import annotations

import logging
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partialmethod
from typing import List, Optional

import mlflow
from tqdm.auto import tqdm

from databricks.rag_eval import context, env_vars, session
from databricks.rag_eval.config import assessment_config, evaluation_config
from databricks.rag_eval.evaluation import (
    assessments,
    entities,
    metrics,
    models,
    traces,
)
from databricks.rag_eval.utils import input_output_utils, rate_limit, rating_utils

_logger = logging.getLogger(__name__)


def run(
    *,
    eval_items: List[entities.EvalItem],
    config: evaluation_config.EvaluationConfig,
    model: Optional[mlflow.pyfunc.PyFuncModel] = None,
) -> List[entities.EvalResult]:
    """
    Run the logic of the eval harness.

    :param eval_items: List of EvalItems
    :param config: The evaluation config
    :param model: Optional model to use for generating responses and traces
    """
    # Disable tqdm progress bar by default so that the progress bars inside MLflow eval_fn do not show
    tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)

    assessments_to_run: List[assessments.Assessment] = _get_assessments_for_configs(
        config.assessment_configs
    )
    eval_results = []
    with ThreadPoolExecutor(
        max_workers=env_vars.RAG_EVAL_MAX_WORKERS.get()
    ) as executor:
        futures = [
            executor.submit(
                _run_single,
                eval_item=eval_item,
                assessments_to_run=assessments_to_run,
                model=model,
            )
            for eval_item in eval_items
        ]

        futures_as_completed = as_completed(futures)
        # Add a progress bar to show the progress of the assessments
        futures_as_completed = tqdm(
            futures_as_completed,
            total=len(futures),
            disable=False,
            desc="Evaluating",
            smoothing=0,  # 0 means using average speed for remaining time estimates
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [Elapsed: {elapsed}, Remaining: {remaining}]",
        )

        for future in futures_as_completed:
            result = future.result()
            eval_results.append(result)
    return _postprocess_eval_results(eval_results)


def _postprocess_eval_results(
    eval_results: List[entities.EvalResult],
) -> List[entities.EvalResult]:
    """
    Postprocess the eval results by:
    1. Moving missing input field errors (identified by "Error[1001]") from error_messages to rationales.
    2. If all error messages for a particular assessment are the same across all eval items, change these errors to null and instead log the error.

    After the completion of ML-41351, we should migrate this logic to run as a pre-check before sending requests to the managed-rag service.
    """
    # Track errors for each assessment
    assessment_error_counts = defaultdict(
        lambda: defaultdict(int)
    )  # assessment_name -> normalized_error_message -> count
    total_assessments = defaultdict(int)  # assessment_name -> count
    error_messages = defaultdict(str)  # assessment_name -> error_message

    # First pass: Count errors and track common errors
    for eval_result in eval_results:
        for assessment_result in eval_result.assessment_results:
            assessment_name = assessment_result.assessment_name
            total_assessments[assessment_name] += 1
            if isinstance(assessment_result, entities.AnswerAssessmentResult):
                rating = assessment_result.rating
                if rating_utils.is_missing_input_error(rating.error_message):
                    normalized_message = rating_utils.normalize_error_message(
                        rating.error_message
                    )
                    assessment_error_counts[assessment_name][normalized_message] += 1
                    error_messages[assessment_name] = rating.error_message
            elif isinstance(assessment_result, entities.RetrievalAssessmentResult):
                for rating in assessment_result.positional_rating.values():
                    if rating_utils.is_missing_input_error(rating.error_message):
                        normalized_message = rating_utils.normalize_error_message(
                            rating.error_message
                        )
                        assessment_error_counts[assessment_name][
                            normalized_message
                        ] += 1
                        error_messages[assessment_name] = rating.error_message

    # Determine common errors
    common_errors = {
        assessment_name: error_messages[assessment_name]
        for assessment_name, errors in assessment_error_counts.items()
        if len(errors) == 1
        and list(errors.values())[0] == total_assessments[assessment_name]
    }

    # Log common errors
    for assessment_name, error_message in common_errors.items():
        missing_fields = rating_utils.extract_missing_fields_from_missing_input_error(
            error_message
        )
        reason = (
            f"missing input fields: {missing_fields}"
            if missing_fields
            else rating_utils.normalize_error_message(error_message)
        )
        session.current_session().append_warning(
            f"Skipped metric '{assessment_name}' due to {reason}"
        )

    # Second pass: Suppress common errors and move others to rationale
    for eval_result in eval_results:
        for assessment_result in eval_result.assessment_results:
            assessment_name = assessment_result.assessment_name
            if assessment_name in common_errors:
                rating_utils.suppress_errors(assessment_result)
            else:
                rating_utils.move_errors_to_rationale(assessment_result)

    return eval_results


def _run_single(
    eval_item: entities.EvalItem,
    assessments_to_run: List[assessments.Assessment],
    model: Optional[mlflow.pyfunc.PyFuncModel] = None,
) -> entities.EvalResult:
    """
    Run the logic of the eval harness for a single eval item.

    :param eval_item: The eval item to evaluate
    :param assessments_to_run: The list of assessments to run
    :param model: Optional model to use for generating responses and traces
    """
    if model:
        eval_item = _populate_model_result_to_eval_item(
            eval_item=eval_item,
            model_result=models.invoke_model(model, eval_item),
        )
        # Skip the evaluation if invoking the model failed
        if eval_item.model_error_message is not None:
            return _no_op_eval_result(eval_item)
    else:
        eval_item = _maybe_populate_eval_item_with_trace(eval_item)
    assessment_log = assessments.generate_llm_assessments(
        eval_item=eval_item,
        assessments=assessments_to_run,
    )
    return metrics.compute_eval_metrics(assessment_log)


def _no_op_eval_result(eval_item: entities.EvalItem) -> entities.EvalResult:
    """
    Create a no-op eval result for the eval item for skipping the evaluation.

    :param eval_item: The eval item to create a no-op eval result for
    :return: The no-op eval result
    """
    return entities.EvalResult(
        eval_item=eval_item,
        assessment_results=[],
        total_input_token_count=None,
        total_output_token_count=None,
        total_token_count=None,
        exact_match=None,
        latency_seconds=None,
        ground_truth_retrieval_metrics={},
        llm_judged_retrieval_metrics={},
        ground_truth_document_ratings=None,
    )


def _populate_model_result_to_eval_item(
    eval_item: entities.EvalItem, model_result: models.ModelResult
) -> entities.EvalItem:
    """
    Populate the model result to the eval item.

    :param eval_item: The eval item to populate the model result
    :param model_result: The model result to populate
    :return: The populated eval item
    """
    return entities.EvalItem(
        question_id=eval_item.question_id,
        question=eval_item.question,
        raw_request=eval_item.raw_request,
        ground_truth_answer=eval_item.ground_truth_answer,
        ground_truth_retrieval_context=eval_item.ground_truth_retrieval_context,
        answer=model_result.response,
        retrieval_context=model_result.retrieval_context,
        trace=model_result.trace,
        model_error_message=model_result.error_message,
    )


def _maybe_populate_eval_item_with_trace(eval_item: entities.EvalItem):
    """
    Populate the eval item by extracting additional information from the trace.

    Keep the existing values in the eval item if they already exist.
    """
    # Skip if the trace is None
    if eval_item.trace is None:
        return eval_item

    return entities.EvalItem(
        question_id=eval_item.question_id,
        question=eval_item.question,
        raw_request=eval_item.raw_request,
        ground_truth_answer=eval_item.ground_truth_answer,
        ground_truth_retrieval_context=eval_item.ground_truth_retrieval_context,
        trace=eval_item.trace,
        model_error_message=eval_item.model_error_message,
        answer=(
            input_output_utils.output_to_string(
                traces.extract_model_output_from_trace(eval_item.trace)
            )
            if eval_item.answer is None
            else eval_item.answer
        ),
        retrieval_context=(
            traces.extract_retrieval_context_from_trace(eval_item.trace)
            if eval_item.retrieval_context is None
            else eval_item.retrieval_context
        ),
    )


def _get_assessments_for_configs(
    assessment_configs: List[assessment_config.AssessmentConfig],
) -> List[assessments.Assessment]:
    """
    Construct a list of assessments for an EvaluationConfig.
    """
    builtin_rate_limiter = _build_rate_limiter_for_assessment()
    custom_rate_limiter = _build_rate_limiter_for_assessment()
    llm_judge_client = context.get_context().build_llm_judge_client()

    results = []
    for assessment_conf in assessment_configs:
        if isinstance(assessment_conf, assessment_config.BuiltinAssessmentConfig):
            results.append(
                assessments.BuiltInAssessment(
                    config=assessment_conf,
                    rate_limiter=builtin_rate_limiter,
                    llm_judge_client=llm_judge_client,
                )
            )
        elif isinstance(
            assessment_conf, assessment_config.EvaluationMetricAssessmentConfig
        ):
            results.append(
                assessments.EvaluationMetricAssessment(
                    config=assessment_conf,
                    rate_limiter=custom_rate_limiter,
                    llm_judge_client=llm_judge_client,
                )
            )
    return results


def _build_rate_limiter_for_assessment() -> rate_limit.RateLimiter:
    """Build a rate limiter for the assessment."""
    # Return a no-op rate limiter if the rate limiter for assessment is not enabled
    if not env_vars.RAG_EVAL_ENABLE_RATE_LIMIT_FOR_ASSESSMENT.get():
        return rate_limit.RateLimiter.no_op()

    # For now, rate limiter config is from environment variables
    rate_limit_config = assessment_config.RateLimitConfig(
        quota=env_vars.RAG_EVAL_RATE_LIMIT_QUOTA.get(),
        time_window_in_seconds=env_vars.RAG_EVAL_RATE_LIMIT_TIME_WINDOW_IN_SECONDS.get(),
    )
    return rate_limit.RateLimiter.build(
        quota=rate_limit_config.quota,
        time_window_in_seconds=rate_limit_config.time_window_in_seconds,
    )
