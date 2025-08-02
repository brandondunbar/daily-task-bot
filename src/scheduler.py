from datetime import datetime
from src.utils import get_today_str


def find_today_task(rows, date_column="Date"):
    """
    Search a list of rows (dicts) for a row matching today's date.

    Args:
        rows (list of dict): The rows pulled from the sheet.
        date_column (str): The name of the column that holds the date string.

    Returns:
        dict | None: The matching row, or None if not found.

    Raises:
        KeyError: If the date_column is missing in any row.
    """
    today = get_today_str()

    for row in rows:
        if row[date_column] == today:
            return row
    return None
