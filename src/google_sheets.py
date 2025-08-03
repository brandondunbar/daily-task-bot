"""
Enables interaction with Google Sheets.
"""

import gspread
from google.oauth2.service_account import Credentials
from src.constants import GOOGLE_CREDENTIALS_PATH


def get_sheet_rows(sheet_config, credentials):
    """
    Connect to a Google Sheet and retrieve all rows from a specified worksheet.

    Args:
        sheet_config (dict): Configuration for the target sheet, including worksheet name.
        credentials (dict): Credentials or a client object for connecting to Google Sheets.

    Returns:
        list: A list of dictionaries representing the worksheet rows.
    """
    client = get_gspread_client(credentials)
    worksheet = client.worksheet(sheet_config["worksheet"])
    return worksheet.get_all_records()


def get_gspread_client(credentials_path=GOOGLE_CREDENTIALS_PATH):
    """Authenticate and return a gspread client using service account credentials."""

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]

    creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
    return gspread.authorize(creds)
