from string import Formatter
from typing import List


def get_variables_from_template(template_str: str) -> List[str]:
    """
    Get the variables from a template string.
    ex. For string "template of {foo} and {bar}", this function will return ['foo', 'bar']
    """
    return [fname for _, fname, _, _ in Formatter().parse(template_str) if fname]
