"""
Enables interaction with Google Sheets.
"""

import gspread
from google.oauth2.service_account import Credentials


def get_sheet_rows(sheet_name: str, spreadsheet_id: str, credentials: Credentials):
    """
    Connect to a Google Sheet and retrieve all rows from a specified worksheet.

    Args:
        sheet_name (str): Name of the worksheet tab.
        spreadsheet_id (str): ID of the target spreadsheet.
        credentials (Credentials): Authenticated service account credentials.

    Returns:
        list: A list of dictionaries representing the worksheet rows.
    """
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(spreadsheet_id)
    worksheet = sheet.worksheet(sheet_name)
    return worksheet.get_all_records()
