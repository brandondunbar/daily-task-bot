"""
Enables interaction with Google Sheets.
"""

import gspread
from google.oauth2.service_account import Credentials
from src.constants import GOOGLE_CREDENTIALS_PATH


def get_sheet_rows(sheet_config):
    """
    Connect to a Google Sheet and retrieve all rows from a specified worksheet.

    Args:
        sheet_config (dict): Configuration for the target sheet, including worksheet name.

    Returns:
        list: A list of dictionaries representing the worksheet rows.
    """
    client = get_gspread_client()
    worksheet = client.open(sheet_config["worksheet"]).sheet1
    return worksheet.get_all_records()


def get_gspread_client(credentials_path=GOOGLE_CREDENTIALS_PATH):
    """Authenticate and return a gspread client using service account credentials.
    
    Args:
        credentials_path (str): The relative or absolute path to the Service
            Account credentials JSON file.

    Returns:
        gspread.Client: An authenticated client object for accessing Google Sheets.

    Raises:
        FileNotFoundError: If the specified credentials file does not exist.
        google.auth.exceptions.GoogleAuthError: If the credentials are invalid
            or authentication fails.
        ValueError: If the credentials file is malformed or missing required fields.
    """

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]

    creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
    return gspread.authorize(creds)
