"""
¤ ~ ^ - levels - ^ ~ ¤
*. - _ of depth _ - .*
'_- _ - _ - _ - _ - _'

A vertical slicing tool for nested data structures of dictionaries and/or lists.

Search for a key in a nested data structure of dictionaries and/or lists and return
the path and value of the key or return the path and value of all keys at a given
depth in a nested dictionary.

Search for a value in a nested data structure of dictionaries and/or lists and return path or depth.

Functions:
    levels: Return a generator that yields the path and value of a nested dictionary at a given depth.
    get_level: Return the depth of a value or key in a nested dictionary.
    search: Return the depth of a value in a nested data structure.
    find_path: Return the path slice of a value in a nested data structure.
"""

import re
from typing import Any, Generator, Hashable, Union


def levels(
    data: Union[dict, list],
    /,
    depth: int = 0,
    *,
    values=False,
    as_glom=False,
    key=None,
    value=None,
    regex_k=None,
    regex_v=None,
) -> Generator[tuple[str, Any], None, None]:
    """Return a generator that yields the path and value of a nested dictionary at a given depth."""

    if not isinstance(data, (dict, list)):
        raise TypeError("data must be a dictionary or a list.")

    exempted_types = (str, int, float)

    def find_key_and_value(
        dct: dict,
        path: list[Hashable],
        depth: int,
    ) -> Generator[tuple[list, Any], None, None]:
        if depth == 0:
            for k, v in dct.items():
                yield path + [k], v
        else:
            for k, v in dct.items():
                if isinstance(v, dict):
                    yield from find_key_and_value(v, path + [k], depth - 1)
                if isinstance(v, list):
                    yield from find_index_and_value(v, path + [k], depth - 1)

    def find_index_and_value(
        lst: list,
        path: list[Hashable],
        depth: int,
    ) -> Generator[tuple[list, Any], None, None]:
        if depth == 0:
            for i, v in enumerate(lst):
                yield path + [i], v
        else:
            for i, v in enumerate(lst):
                if isinstance(v, dict):
                    yield from find_key_and_value(v, path + [i], depth - 1)
                if isinstance(v, list):
                    yield from find_index_and_value(v, path + [i], depth - 1)

    start_func = find_key_and_value if isinstance(data, dict) else find_index_and_value

    for path, val in start_func(data, [], depth):
        if key is not None and key not in path:
            continue

        if regex_k is not None and not re.search(regex_k, str(path)):
            continue

        if value is not None and value != val:
            continue

        if regex_v is not None and not re.search(regex_v, str(val)):
            continue

        if not values:
            if isinstance(val, dict):
                val = "{...}"
            elif isinstance(val, list):
                val = "[...]"
            elif isinstance(val, exempted_types):
                pass
            else:
                val = "object"

        if as_glom:
            slices = ".".join([str(k) for k in path])
        else:
            slices = "".join(
                [f"['{k}']" if isinstance(k, str) else f"[{k}]" for k in path]
            )

        yield slices, val


def get_level(dct: dict, /, value: Any = None, key: Any = None) -> int:
    """Return the depth of a value or key in a nested dictionary."""

    if key is None and value is None:
        raise ValueError("Either key or value must be provided.")

    def find_key_and_value(dct: dict, depth: int) -> int:
        for k, v in dct.items():
            if v == value or k == key:
                return depth
            if isinstance(v, dict):
                if (result := find_key_and_value(v, depth + 1)) is not None:
                    return result

    level = find_key_and_value(dct, 0)

    if level is None:
        raise ValueError("Key or value not found.")

    return level


def search(data: Union[dict, list], /, value: Any) -> int:
    """Return the depth of a value in a nested dictionary or list."""

    if not isinstance(data, (dict, list)):
        raise TypeError("data must be a dictionary or a list.")

    def find_key_and_value(
        dct: dict,
        depth: int,
    ) -> int:
        for k, v in dct.items():
            if v == value:
                return depth
            if isinstance(v, dict):
                if (result := find_key_and_value(v, depth + 1)) is not None:
                    return result
            if isinstance(v, list):
                if (result := find_index_and_value(v, depth + 1)) is not None:
                    return result

    def find_index_and_value(
        lst: list,
        depth: int,
    ) -> int:
        for i, v in enumerate(lst):
            if v == value:
                return depth
            if isinstance(v, dict):
                if (result := find_key_and_value(v, depth + 1)) is not None:
                    return result
            if isinstance(v, list):
                if (result := find_index_and_value(v, depth + 1)) is not None:
                    return result

    start_func = find_key_and_value if isinstance(data, dict) else find_index_and_value

    level = start_func(data, 0)

    if level is None:
        raise ValueError("Value not found.")

    return level


def find_path(
    data: Union[dict, list], /, value: Any, *, as_glom: bool = False
) -> list[Hashable]:
    """Return the path of a value in a nested data structure."""

    level = search(data, value)
    path, value = next(levels(data, depth=level, value=value, as_glom=as_glom))

    if path is None:
        raise ValueError("Key or value not found.")

    return path


def contains(data: Union[dict, list], /, value: Any) -> bool:
    """Return True if the value is in the nested data structure."""

    try:
        search(data, value)
    except ValueError:
        return False

    return True
