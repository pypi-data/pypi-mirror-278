import dataclasses
from typing import List, Optional

from databricks.rag_eval.config.assessment_config import (
    AssessmentType,
    BuiltinAssessmentConfig,
)

# ================ Answer Assessments ================
GROUNDEDNESS = BuiltinAssessmentConfig(
    assessment_name="groundedness",
    assessment_type=AssessmentType.ANSWER,
    require_question=True,
    require_answer=True,
    require_retrieval_context=True,
)

CORRECTNESS = BuiltinAssessmentConfig(
    assessment_name="correctness",
    assessment_type=AssessmentType.ANSWER,
    require_question=True,
    require_answer=True,
    require_ground_truth_answer=True,
)

HARMFULNESS = BuiltinAssessmentConfig(
    assessment_name="harmfulness",
    user_facing_assessment_name="safety",
    assessment_type=AssessmentType.ANSWER,
    require_question=True,
    require_answer=True,
    flip_rating=True,
)

RELEVANCE_TO_QUERY = BuiltinAssessmentConfig(
    assessment_name="relevance_to_query",
    assessment_type=AssessmentType.ANSWER,
    require_question=True,
    require_answer=True,
)

# ================ Retrieval Assessments ================
CHUNK_RELEVANCE = BuiltinAssessmentConfig(
    assessment_name="chunk_relevance",
    assessment_type=AssessmentType.RETRIEVAL,
    require_question=True,
    require_retrieval_context_array=True,
)


def builtin_assessment_configs() -> List[BuiltinAssessmentConfig]:
    """Returns the list of built-in assessment configs"""
    return [
        HARMFULNESS,
        GROUNDEDNESS,
        CORRECTNESS,
        RELEVANCE_TO_QUERY,
        CHUNK_RELEVANCE,
    ]


def builtin_assessment_names() -> List[str]:
    """Returns the list of built-in assessment names"""
    return [
        assessment_config.assessment_name
        for assessment_config in builtin_assessment_configs()
    ]


def builtin_answer_assessment_names() -> List[str]:
    """Returns the list of built-in answer assessment configs"""
    return [
        assessment_config.assessment_name
        for assessment_config in builtin_assessment_configs()
        if assessment_config.assessment_type == AssessmentType.ANSWER
    ]


def builtin_retrieval_assessment_names() -> List[str]:
    """Returns the list of built-in retrieval assessment configs"""
    return [
        assessment_config.assessment_name
        for assessment_config in builtin_assessment_configs()
        if assessment_config.assessment_type == AssessmentType.RETRIEVAL
    ]


def get_builtin_assessment_config_with_service_assessment_name(
    name: str,
) -> BuiltinAssessmentConfig:
    """
    Returns the built-in assessment config with the given service assessment name
    :param name: The service assessment name of the assessment
    :returns: The built-in assessment config
    """
    for assessment_config in builtin_assessment_configs():
        if assessment_config.assessment_name == name:
            return assessment_config

    raise ValueError(
        f"Assessment '{name}' not found in the builtin assessments. "
        f"Available assessments: {builtin_assessment_names()}."
    )


def get_builtin_assessment_config_with_eval_assessment_name(
    name: str,
) -> BuiltinAssessmentConfig:
    """
    Returns the built-in assessment config with the given eval assessment name
    :param name: The eval assessment name of the assessment
    :returns: The built-in assessment config
    """
    for assessment_config in builtin_assessment_configs():
        if translate_to_eval_assessment_name(assessment_config.assessment_name) == name:
            return assessment_config

    available_assessment_names = [
        translate_to_eval_assessment_name(name) for name in builtin_assessment_names()
    ]
    raise ValueError(
        f"Assessment '{name}' not found in the builtin assessments. "
        f"Available assessments: {available_assessment_names}."
    )


def get_builtin_assessment_config_with_name_with_instruction(
    eval_assessment_name: str,
    domain_instructions: Optional[str],
) -> BuiltinAssessmentConfig:
    """Returns the built-in assessment config with the given user-facing name and adds on an instruction"""
    assessment_config = get_builtin_assessment_config_with_eval_assessment_name(
        eval_assessment_name
    )
    return dataclasses.replace(
        assessment_config, domain_instructions=domain_instructions
    )


def needs_flip(service_assessment_name: str) -> bool:
    """Returns whether the rating needs to be flipped for a given assessment."""
    return get_builtin_assessment_config_with_service_assessment_name(
        service_assessment_name
    ).flip_rating


def translate_to_eval_assessment_name(service_assessment_name: str) -> str:
    """
    Given a service assessment name, returns the corresponding user-facing assessment name. If no
    user-facing name is specified, assume the service name is the user-facing name.
    """
    if service_assessment_name not in builtin_assessment_names():
        return service_assessment_name
    assessment = get_builtin_assessment_config_with_service_assessment_name(
        service_assessment_name
    )
    return (
        assessment.user_facing_assessment_name
        if assessment.user_facing_assessment_name is not None
        else assessment.assessment_name
    )
