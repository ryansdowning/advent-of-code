from typing import Any, Callable

Splitter = tuple[str, Callable[[list[str]], Any] | None]


def _recursively_split_aux(strings: list[str], splitters: list[Splitter]) -> list:
    """
    Auxiliary function for recursively splitting a string.

    Applies the splitter operation to the given list of strings, and then recurses by applying the remaining splitters
    to the resulting list of strings.

    Args:
        strings: List of strings to apply the head splitter operation to.
        splitters: Remaining splitter operations.

    Returns:
        List of strings, or nested list of strings.
    """
    if len(splitters) == 0:
        return strings

    (split_str, func), *splitters = splitters
    if func is None:
        func = lambda x: x
    return [_recursively_split_aux(func(string.split(split_str)), splitters) for string in strings]


def recursively_split(string: str, splitters: list[Splitter]) -> list:
    """
    Recursively splits a string given a list of splitters.

    A splitter is a tuple of the split string, and a processing function to perform on the resulting list of strings.
    Because this function acts recursively, each splitter adds a dimension to the final list output. For example, with
    one splitter, this returns a 1-D list, and with two splitters, this returns a 2-D list, and so on (assuming the
    processing function returns the same type as the input, a list of strings).

    Args:
        string: The string to be recursively split
        splitters: List of tuples defining the splitter operations.

    Returns:
        List of strings, or nested list of strings.
    """
    return _recursively_split_aux([string], splitters)[0]
