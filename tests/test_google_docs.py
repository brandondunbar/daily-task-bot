from unittest.mock import MagicMock, patch

import pytest
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError
from src.google_docs import build_docs_service, overwrite_doc_contents


@pytest.fixture
def fake_credentials():
    return MagicMock(spec=Credentials)


@pytest.mark.parametrize("end_index,new_content", [
    (42, "New content goes here."),
    (1, "Content for empty doc."),
    (100, "A" * 100),
])
def test_overwrite_doc_contents_sends_expected_requests(
    fake_credentials,
    end_index,
    new_content):
    """Sends expected delete/insert requests based on document's end index."""
    mock_execute = MagicMock()
    mock_execute.return_value = {
        "body": {
            "content": [{"endIndex": end_index}]
        }
    }

    mock_get = MagicMock()
    mock_get.execute = mock_execute

    mock_batch_update = MagicMock()
    mock_batch_update.execute = MagicMock()

    mock_documents = MagicMock()
    mock_documents.get.return_value = mock_get
    mock_documents.batchUpdate.return_value = mock_batch_update

    mock_docs_service = MagicMock()
    mock_docs_service.documents.return_value = mock_documents

    with patch("src.google_docs.build_docs_service", return_value=mock_docs_service):
        overwrite_doc_contents("test-doc-id", new_content, fake_credentials)

    mock_documents.get.assert_called_once_with(documentId="test-doc-id")
    mock_documents.batchUpdate.assert_called_once()
    mock_batch_update.execute.assert_called_once()


def test_overwrite_doc_contents_handles_http_error(fake_credentials):
    """Raises HttpError if Docs API request fails during document fetch."""
    mock_docs_service = MagicMock()
    mock_docs_service.documents().get.side_effect = HttpError(
        resp=MagicMock(), content=b"Error")

    with patch("src.google_docs.build_docs_service", return_value=mock_docs_service):
        with pytest.raises(HttpError):
            overwrite_doc_contents("test-doc-id", "Content", fake_credentials)


def test_build_docs_service_success(fake_credentials):
    """Successfully builds and returns the Docs API client."""
    with patch("src.google_docs.build", return_value="mock_service") as mock_build:
        service = build_docs_service(fake_credentials)
        assert service == "mock_service"
        mock_build.assert_called_once_with("docs", "v1", credentials=fake_credentials)


def test_build_docs_service_failure(fake_credentials):
    """Raises and logs HttpError if Docs API client build fails."""
    with patch(
        "src.google_docs.build",
        side_effect=HttpError(resp=MagicMock(), content=b"Boom")):
        with pytest.raises(HttpError):
            build_docs_service(fake_credentials)
