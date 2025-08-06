import pytest
from unittest.mock import MagicMock
from src.google_sheets import get_sheet_rows
from google.oauth2.service_account import Credentials


class MockWorksheet:
    def get_all_records(self):
        return [
            {"Date": "2025-08-01", "Problem Title": "Test Problem 1"},
            {"Date": "2025-08-02", "Problem Title": "Test Problem 2"},
        ]


class MockSheet:
    def __init__(self, expected_name):
        self.expected_name = expected_name

    def worksheet(self, name):
        if name != self.expected_name:
            raise ValueError("Worksheet not found")
        return MockWorksheet()


class MockClient:
    def __init__(self, expected_name):
        self.expected_name = expected_name

    def open_by_key(self, key):
        return MockSheet(self.expected_name)


@pytest.fixture
def fake_credentials():
    return MagicMock(spec=Credentials)


def test_get_sheet_rows_returns_expected_data(monkeypatch, fake_credentials):
    expected_sheet_name = "Schedule"
    spreadsheet_id = "fake-id"

    monkeypatch.setattr("src.google_sheets.gspread.authorize", lambda creds: MockClient(expected_sheet_name))

    rows = get_sheet_rows(expected_sheet_name, spreadsheet_id, fake_credentials)

    assert isinstance(rows, list)
    assert len(rows) == 2
    assert rows[0]["Problem Title"] == "Test Problem 1"
    assert rows[1]["Date"] == "2025-08-02"
