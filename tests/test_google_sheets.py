import pytest
from src.google_sheets import get_sheet_rows


class MockWorksheet:
    """
    A mock worksheet that simulates a Google Sheets worksheet object.
    Provides static row data via get_all_records().
    """

    def get_all_records(self):
        """
        Return a static list of row dictionaries representing worksheet data.

        Returns:
            list: A list of dictionaries with mock data.
        """

        return [
            {"Date": "2025-08-01", "Problem Title": "Test Problem 1"},
            {"Date": "2025-08-02", "Problem Title": "Test Problem 2"}
        ]


class MockSheetClient:
    """
    A mock gspread client that returns a mock worksheet.
    Used to simulate accessing a Google Sheets worksheet by name.
    """

    def __init__(self, worksheet_name):
        self.worksheet_name = worksheet_name

        def worksheet(self, name):
            """
            Simulate worksheet lookup. Returns a mock worksheet if the name matches.

            Args:
                name (str): The name of the worksheet to retrieve.

            Returns:
                MockWorksheet: A mock worksheet object.

            Raises:
                ValueError: If the worksheet name does not match.
            """

            if name == self.worksheet_name:
                return MockWorksheet()
            raise ValueError("Worksheet not found")


@pytest.fixture
def sample_config():
    return {
        "name": "Test Sheet",
        "id": "fake-id",
        "worksheet": "Schedule",
        "date_column": "Date",
        "output_folder_id": "folder-id",
        "template_blurb": "{{ Problem Title }}",
        "column_mapping": {
            "Problem Title": "Problem Title"
        }
    }


def test_get_sheet_rows_returns_expected_data(monkeypatch, sample_config):
    """
    Test that get_sheet_rows returns expected data using a mocked Sheet client.

    Args:
        monkeypatch (pytest.MonkeyPatch): Used to patch gspread client.
        sample_config (dict): Example sheet config.
    """
    
    monkeypatch.setattr("src.google_sheets.get_gspread_client", lambda _: MockSheetClient("Schedule"))

    rows = get_sheet_rows(sample_config, credentials={})
    assert isinstance(rows, list)
    assert len(rows) == 2
    assert rows[0]["Problem Title"] == "Test Problem 1"
    assert rows[1]["Date"] == "2025-08-02"
