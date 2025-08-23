"""Provides a Google service account credential loader.

Defines `get_service_account_credentials()` to load credentials using
a service account JSON file and optional scopes for Google APIs.
"""

from google.oauth2.service_account import Credentials

from src.constants import GOOGLE_CREDENTIALS_PATH
from src.observability.logging_setup import get_logger

log = get_logger(__name__)


def get_service_account_credentials(scopes=None) -> Credentials:
    """Load and return Google service account credentials with the specified scopes.

    Args:
        scopes (list, optional): List of OAuth2 scopes. Defaults to basic
        Sheets and Docs scopes.

    Returns:
        Credentials: Authenticated service account credentials.
    """
    if scopes is None:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/documents"
        ]

    try:
        creds = Credentials.from_service_account_file(
            GOOGLE_CREDENTIALS_PATH,
            scopes=scopes
        )
        log.info("credentials_loaded", path=GOOGLE_CREDENTIALS_PATH, scopes=scopes)
        return creds
    except Exception as e:
        log.exception(
            "credentials_load_failed",
            path=GOOGLE_CREDENTIALS_PATH,
            error=str(e))
        raise
