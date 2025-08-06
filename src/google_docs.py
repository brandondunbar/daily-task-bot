from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError
from src.template import render_template


def build_docs_service(credentials: Credentials):
    """
    Return an authenticated Google Docs API service using provided credentials.

    Args:
        credentials (Credentials): Google service account credentials.

    Returns:
        googleapiclient.discovery.Resource: Google Docs service object.
    """
    return build("docs", "v1", credentials=credentials)


def overwrite_doc_contents(document_id: str, new_content: str, credentials: Credentials):
    """
    Overwrite the entire contents of a Google Doc with new text.

    Args:
        document_id (str): The ID of the document to modify.
        new_content (str): The new text content to insert into the document.
        credentials (Credentials): Authenticated service account credentials.
    """
    docs_service = build_docs_service(credentials)

    try:
        doc = docs_service.documents().get(documentId=document_id).execute()
        end_index = doc.get("body", {}).get("content", [])[-1].get("endIndex", 1)

        requests = [
            {
                "deleteContentRange": {
                    "range": {
                        "startIndex": 1,
                        "endIndex": end_index - 1
                    }
                }
            },
            {
                "insertText": {
                    "location": {"index": 1},
                    "text": new_content
                }
            }
        ]

        docs_service.documents().batchUpdate(
            documentId=document_id,
            body={"requests": requests}
        ).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")
        raise
