"""Google Sheets helpers for reading worksheet rows.

This module exposes a thin wrapper that authorizes a Sheets client with a
service account and returns all records from a specific worksheet tab.
"""


from typing import Any, Dict, List

import gspread
from google.oauth2.service_account import Credentials


def get_sheet_rows(
    sheet_name: str,
    spreadsheet_id: str,
    credentials: Credentials,
) -> List[Dict[str, Any]]:
    """Return all rows from a worksheet as a list of dictionaries.

    Authorizes a gspread client using the provided service account credentials,
    opens the spreadsheet by ID, selects the named worksheet tab, and returns
    its records, where each row is mapped by the header row.

    Args:
        sheet_name: Name of the worksheet tab to read.
        spreadsheet_id: The Google Sheets spreadsheet ID.
        credentials: Authenticated service account credentials.

    Returns:
        A list of dictionaries, one per row, keyed by column header.

    Raises:
        SpreadsheetNotFound: If the spreadsheet ID is invalid or inaccessible.
        WorksheetNotFound: If the named worksheet does not exist.
        APIError: For other Google Sheets API-related errors (quota, auth, etc.).
    """
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(spreadsheet_id)
    worksheet = sheet.worksheet(sheet_name)
    return worksheet.get_all_records()
