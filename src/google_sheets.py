"""
Enables interaction with Google Sheets.
"""

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


def get_gspread_client(credentials):
    """
    Placeholder to represent gspread client setup.
    In actual implementation, this would authorize and return a gspread client.

    Args:
        credentials (dict): Credential object or data to authorize access.

    Returns:
        gspread.Client: A Google Sheets API client.
    """
    raise NotImplementedError("This function should return an authorized gspread client.")
