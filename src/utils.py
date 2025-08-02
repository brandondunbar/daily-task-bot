"""
Utility functions.
"""

from datetime import datetime


def get_today_str(fmt="%Y-%m-%d") -> str:
    """
    Return today's date as a string formatted by the given format string.

    Args:
        fmt (str): The format to use (default is "%Y-%m-%d").

    Returns:
        str: Today's date as a string.
    """
    return datetime.today().strftime(fmt)
