"""Google Docs API helpers for building a service client and updating documents.

This module provides utilities to construct an authenticated Docs service
and to overwrite a document's contents with new text.
"""
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def build_docs_service(credentials: Credentials):
    """Create an authenticated Google Docs API service.

    Args:
        credentials: Google service account credentials.

    Returns:
        Resource: An authenticated Google Docs service client.

    Raises:
        HttpError: If the underlying client initialization fails.
    """
    return build("docs", "v1", credentials=credentials)


def overwrite_doc_contents(
    document_id: str,
    new_content: str,
    credentials: Credentials,
) -> None:
    """Overwrite the entire contents of a Google Doc with new text.

    Fetches the document to determine its current end index, deletes existing
    content (if any), and inserts the provided `new_content` at the start.

    Args:
        document_id: The ID of the Google Doc to modify.
        new_content: The new text content to insert into the document.
        credentials: Authenticated service account credentials.

    Raises:
        HttpError: If the Google Docs API request fails.
    """
    docs_service = build_docs_service(credentials)

    try:
        doc = docs_service.documents().get(documentId=document_id).execute()
        end_index = doc.get("body", {}).get("content", [])[-1].get("endIndex", 1)

        requests = []

        # Only add delete if there's something to delete
        if end_index > 2:
            requests.append({
                "deleteContentRange": {
                    "range": {
                        "startIndex": 1,
                        "endIndex": end_index - 1
                    }
                }
            })

        requests.append({
            "insertText": {
                "location": {"index": 1},
                "text": new_content
            }
        })

        docs_service.documents().batchUpdate(
            documentId=document_id,
            body={"requests": requests}
        ).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")
        raise
