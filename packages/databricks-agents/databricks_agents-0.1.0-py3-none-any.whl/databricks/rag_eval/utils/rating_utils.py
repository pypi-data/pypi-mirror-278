"""Helper functions for dealing with ratings."""

import re
from typing import Optional

from databricks.rag_eval.evaluation import entities


def _extract_error_code(error_message: Optional[str]) -> Optional[str]:
    """
    Extract the error code from the error message.
    """
    if error_message is None:
        return None
    match = re.match(r"Error\[(\d+)]", error_message)
    return match.group(1) if match else None


def is_missing_input_error(error_message: Optional[str]) -> bool:
    """
    Check if the error message is due to missing input fields (Error[1001]).
    """
    return _extract_error_code(error_message) == "1001"


def extract_missing_fields_from_missing_input_error(error_message: str) -> str:
    """
    Extract the missing field from the missing input error message.

    The missing field is the string between "Missing input fields: " and ", Reference ID:" in the error message.
    """
    pattern = (
        r"Error\[\d+\]: Missing input fields: ([\w, ]+), Reference ID: [\w.,!?;:-]+"
    )

    # Search for the pattern in the message
    match = re.search(pattern, error_message)

    # If a match is found, extract the groups
    if match:
        missing_fields = match.group(1)
        return missing_fields
    else:
        return ""


def normalize_error_message(error_message: str) -> str:
    """
    Normalize the error message by removing the Reference ID part.

    The Reference ID is a UUID generated for every Armeria service call. We assume any string
    after "Reference ID: " with the character set described in the regex below is a Reference ID.
    """
    return re.sub(r", Reference ID: [\w.,!?;:-]+", "", error_message)


def suppress_errors(assessment_result: entities.AssessmentResult):
    """
    Suppress all errors for an assessment result by setting error_message to None.
    """
    if isinstance(assessment_result, entities.AnswerAssessmentResult):
        assessment_result.rating.error_message = None
    elif isinstance(assessment_result, entities.RetrievalAssessmentResult):
        for rating in assessment_result.positional_rating.values():
            rating.error_message = None


def move_errors_to_rationale(assessment_result):
    """
    Move missing input field errors from error_messages to rationales for an assessment result.
    """
    if isinstance(assessment_result, entities.AnswerAssessmentResult):
        rating = assessment_result.rating
        if is_missing_input_error(rating.error_message):
            rating.rationale = rating.error_message
            rating.error_message = None
    elif isinstance(assessment_result, entities.RetrievalAssessmentResult):
        for rating in assessment_result.positional_rating.values():
            if is_missing_input_error(rating.error_message):
                rating.rationale = rating.error_message
                rating.error_message = None
