import pytest
from src.auth import get_service_account_credentials
from src.constants import GOOGLE_CREDENTIALS_PATH
from google.oauth2.service_account import Credentials


def test_get_service_account_credentials_default_scopes(monkeypatch):
    class DummyCredentials:
        def __init__(self, filename, scopes):
            self.filename = filename
            self.scopes = scopes

    monkeypatch.setattr(
        "src.auth.Credentials.from_service_account_file",
        lambda path, scopes: DummyCredentials(path, scopes)
    )

    creds = get_service_account_credentials()

    assert creds.filename == GOOGLE_CREDENTIALS_PATH
    assert "https://www.googleapis.com/auth/spreadsheets.readonly" in creds.scopes
    assert "https://www.googleapis.com/auth/documents" in creds.scopes


def test_get_service_account_credentials_custom_scopes(monkeypatch):
    class DummyCredentials:
        def __init__(self, filename, scopes):
            self.filename = filename
            self.scopes = scopes

    monkeypatch.setattr(
        "src.auth.Credentials.from_service_account_file",
        lambda path, scopes: DummyCredentials(path, scopes)
    )

    custom_scopes = ["scope1", "scope2"]
    creds = get_service_account_credentials(scopes=custom_scopes)

    assert creds.filename == GOOGLE_CREDENTIALS_PATH
    assert creds.scopes == custom_scopes
