"""Task scheduling helpers for selecting a row that matches today's date.

This module currently provides a utility to scan worksheet rows and return
the one scheduled for today, based on a configured date column.
"""

from typing import Any, Dict, List, Optional

from src.utils import get_today_str


def find_today_task(
    rows: List[Dict[str, Any]],
    date_column: str = "Date",
) -> Optional[Dict[str, Any]]:
    """Return the first row whose date equals today's date string.

    Compares each row's `date_column` value to `get_today_str()`. The date
    format must match whatever `get_today_str()` returns (typically an ISO-
    like string you define elsewhere).

    Args:
        rows: Rows pulled from the sheet, each as a dict keyed by column header.
        date_column: Column name that holds the date string. Defaults to "Date".

    Returns:
        The matching row if found; otherwise, None.

    Raises:
        KeyError: If `date_column` is missing in any examined row.
    """
    today = get_today_str()

    for row in rows:
        if date_column not in row:
            raise KeyError(f"Missing required date column: {date_column!r}")
        if row[date_column] == today:
            return row

    return None
