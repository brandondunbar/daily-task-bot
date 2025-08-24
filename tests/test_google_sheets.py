from unittest.mock import MagicMock, patch

import pytest
from google.oauth2.service_account import Credentials
from src.google_sheets import get_sheet_rows


class MockWorksheet:
    def __init__(self, data):
        self._data = data

    def get_all_records(self):
        return self._data


class MockSheet:
    def __init__(self, expected_name, data):
        self.expected_name = expected_name
        self._data = data

    def worksheet(self, name):
        if name != self.expected_name:
            raise ValueError("Worksheet not found")
        return MockWorksheet(self._data)


class MockClient:
    def __init__(self, expected_name, data):
        self.expected_name = expected_name
        self._data = data

    def open_by_key(self, key):
        return MockSheet(self.expected_name, self._data)


@pytest.fixture
def fake_credentials():
    return MagicMock(spec=Credentials)


@pytest.mark.parametrize("sheet_name,data", [
    ("Schedule", [{"Date": "2025-08-01"}, {"Date": "2025-08-02"}]),
    ("Progress", [{"Status": "Done"}]),
    ("Empty", []),
])
def test_get_sheet_rows_returns_expected_data(
    monkeypatch, fake_credentials, sheet_name, data):
    """Returns expected records for various sheet names and row data."""
    monkeypatch.setattr("src.google_sheets.gspread.authorize",
                        lambda creds: MockClient(sheet_name, data))
    rows = get_sheet_rows(sheet_name, "spreadsheet-id", fake_credentials)
    assert rows == data


def test_get_sheet_rows_raises_on_invalid_worksheet(monkeypatch, fake_credentials):
    """Raises ValueError if the worksheet name is incorrect."""
    monkeypatch.setattr("src.google_sheets.gspread.authorize",
                        lambda creds: MockClient("ExpectedSheet", []))
    with pytest.raises(ValueError):
        get_sheet_rows("WrongSheet", "spreadsheet-id", fake_credentials)


def test_get_sheet_rows_logs_exception(monkeypatch, fake_credentials):
    """Logs exception and raises when worksheet access fails."""
    with patch("src.google_sheets.gspread.authorize",
               side_effect=Exception("Auth failure")):
        with patch("src.google_sheets.log.exception") as mock_log:
            with pytest.raises(Exception):
                get_sheet_rows("AnySheet", "spreadsheet-id", fake_credentials)
            mock_log.assert_called_once()
