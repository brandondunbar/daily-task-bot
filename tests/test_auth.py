import pytest
from src.auth import get_service_account_credentials
from src.constants import GOOGLE_CREDENTIALS_PATH


def test_get_service_account_credentials_default_scopes(monkeypatch):
    """Loads credentials with default Sheets and Docs scopes."""
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
    """Loads credentials using explicitly provided scopes."""
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


def test_get_service_account_credentials_raises_and_logs(monkeypatch):
    """Raises and logs error when loading credentials fails."""
    monkeypatch.setattr(
        "src.auth.Credentials.from_service_account_file",
        lambda path, scopes: (_ for _ in ()).throw(Exception("Boom"))
    )

    with pytest.raises(Exception, match="Boom"):
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("src.auth.log.exception", lambda *args, **kwargs: None)
            get_service_account_credentials()
