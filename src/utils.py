"""Utility functions for date and time formatting.

Currently provides helpers for returning today's date string in a configurable format.
"""

from datetime import datetime


def get_today_str(fmt: str = "%Y-%m-%d") -> str:
    """Return today's date as a formatted string.

    Args:
        fmt: Format string following `datetime.strftime` syntax.
            Defaults to "%Y-%m-%d".

    Returns:
        Today's date as a string formatted according to `fmt`.
    """
    return datetime.today().strftime(fmt)
