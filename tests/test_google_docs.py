import pytest
from unittest.mock import MagicMock, patch
from googleapiclient.errors import HttpError
from src.google_docs import overwrite_doc_contents
from google.oauth2.service_account import Credentials


@pytest.fixture
def fake_credentials():
    return MagicMock(spec=Credentials)


def test_overwrite_doc_contents_sends_expected_requests(fake_credentials):
    mock_execute = MagicMock()
    mock_execute.return_value = {
        "body": {
            "content": [{"endIndex": 42}]
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
        overwrite_doc_contents("test-doc-id", "New content goes here.", fake_credentials)

    mock_documents.get.assert_called_once_with(documentId="test-doc-id")
    mock_documents.batchUpdate.assert_called_once()
    mock_batch_update.execute.assert_called_once()


def test_overwrite_doc_contents_handles_http_error(fake_credentials):
    mock_docs_service = MagicMock()
    mock_docs_service.documents().get.side_effect = HttpError(resp=MagicMock(), content=b"Error")

    with patch("src.google_docs.build_docs_service", return_value=mock_docs_service):
        with pytest.raises(HttpError):
            overwrite_doc_contents("test-doc-id", "Content", fake_credentials)
