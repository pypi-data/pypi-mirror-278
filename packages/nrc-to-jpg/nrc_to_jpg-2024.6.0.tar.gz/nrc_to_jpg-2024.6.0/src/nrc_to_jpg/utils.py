"""Utility functions (for string manipulation, formatting, and processing) for github-backup."""

from __future__ import annotations

from string import Formatter
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable


def join_wrap(iterable: Iterable[Any], sep: str, wrap: str) -> str:
    """Joins elements of an iterable into a string, wrapping each element with specified characters.

    Args:
        iterable: An iterable containing elements to be joined.
        sep: The separator between elements in the resulting string.
        wrap: The characters used to wrap each element.

    Returns:
        The resulting joined string.
    """
    return sep.join([f"{wrap}{item}{wrap}" for item in iterable])


def get_format_fields(s: str) -> set[str]:
    """Extracts format fields from a string.

    Args:
        s: The input string containing format fields.

    Returns:
        A set of format fields present in the input string.
    """
    return {field for _, field, _, _ in Formatter().parse(s) if field}
