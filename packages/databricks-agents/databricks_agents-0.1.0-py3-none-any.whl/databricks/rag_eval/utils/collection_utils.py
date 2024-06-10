"""Utilities for manipulating collections."""

from typing import Any, Dict, List, Mapping


def omit_keys(d: Mapping[str, Any], keys: List[str]) -> Dict[str, Any]:
    """
    Omit keys from a dictionary.
    :param d:
    :param keys:
    :return: A new dictionary with the keys removed.
    """
    return {k: v for k, v in d.items() if k not in keys}


def position_map_to_list(d: Mapping[int, Any], default: Any = None) -> List[Any]:
    """
    Convert a position map to a list ordered by position. Missing positions are filled with the default value.
    Position starts from 0.

    e.g. {0: 'a', 1: 'b', 3: 'c'} -> ['a', 'b', default, 'c']

    :param d: A position map.
    :param default: The default value to fill missing positions.
    :return: A list of values in the map.
    """
    length = max(d.keys(), default=-1) + 1
    return [d.get(i, default) for i in range(length)]
