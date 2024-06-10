""" Utilities to validate and manipulate model inputs and outputs. """

from typing import Any, Dict, List, NewType, Optional, Union

import pandas as pd

ModelInput = NewType("ModelInput", Union[Dict[str, Any], str])
ModelOutput = NewType(
    "ModelOutput", Optional[Union[Dict[str, Any], str, List[Dict[str, Any]], List[str]]]
)


def input_to_string(data: ModelInput) -> str:
    """Converts a model input to a string. The following input formats are accepted:
    1. str
    2. Dictionary representations of ChatCompletionRequest
    3. Dictionary representations of SplitChatMessagesRequest

    This method performs the minimal validations required to extract the input string.
    """
    if isinstance(data, str):
        return data
    if not isinstance(data, Dict):
        raise ValueError(f"Expected a dictionary, got {type(data)}")
    # ChatCompletionRequest input
    if (
        "messages" in data
        and len(data["messages"]) > 0
        and data["messages"][-1].get("content") is not None
    ):
        return data["messages"][-1]["content"]
    # SplitChatMessagesRequest input
    if "query" in data:
        return data["query"]
    raise ValueError(f"Invalid input: {data}")


def is_valid_input(data: ModelInput) -> bool:
    """Checks whether an input is considered valid for the purposes of evaluation.

    Valid input formats are described in the docstring for `input_to_string`.
    """
    try:
        return input_to_string(data) is not None
    except ValueError:
        return False


def is_none_or_nan(value: Any) -> bool:
    """Checks whether a value is None or NaN."""
    # isinstance(value, float) check is needed to ensure that pd.isna is not called on an array.
    return value is None or (isinstance(value, float) and pd.isna(value))


def output_to_string(data: ModelOutput) -> Optional[str]:
    """Converts a model output to a string. The following output formats are accepted:
    1. str
    2. Dictionary representations of ChatCompletionResponse
    3. Dictionary representations of StringResponse

    If None is passed in, None is returned.

    This method performs the minimal validations required to extract the output string.
    """
    if is_none_or_nan(data):
        return None
    if isinstance(data, str):
        return data
    if isinstance(data, list) and len(data) > 0:
        # PyFuncModel.predict may wrap the output in a list
        return output_to_string(data[0])
    if not isinstance(data, Dict):
        raise ValueError(f"Expected a dictionary, got {type(data)}")
    # ChatCompletionResponse output
    if (
        "choices" in data
        and len(data["choices"]) > 0
        and data["choices"][0].get("message") is not None
        and data["choices"][0]["message"].get("content") is not None
    ):
        return data["choices"][0]["message"]["content"]
    # StringResponse output
    if "content" in data:
        return data["content"]

    raise ValueError(f"Invalid output: {data}")


def is_valid_output(data: ModelOutput) -> bool:
    """Checks whether an output is considered valid for the purposes of evaluation.

    Valid output formats are described in the docstring for `output_to_string`.
    """
    try:
        output_to_string(data)
        return True
    except ValueError:
        return False
