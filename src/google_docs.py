from jinja2 import Template
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from src.constants import GOOGLE_CREDENTIALS_PATH


def render_template_to_string(template_str, row):
    """
    Render a template string with values from a task row.

    Args:
        template_str (str): A Jinja2 template string.
        row (dict): A dictionary containing values to inject into the template.

    Returns:
        str: The rendered string.
    """
    template = Template(template_str)
    return template.render(**row)


def build_docs_service():
    """Return an authenticated Google Docs API service."""
    scopes = [
        "https://www.googleapis.com/auth/documents",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH, scopes=scopes)
    return build("docs", "v1", credentials=creds)


def edit_title(document_id, new_title):
    """
    Update the title of a Google Doc.

    Args:
        document_id (str): The ID of the document to update.
        new_title (str): The new title to set for the document.
    """
    docs_service = build_docs_service()
    docs_service.documents().update(
        documentId=document_id,
        body={"title": new_title}
    ).execute()


def overwrite_doc_contents(document_id, new_content):
    """
    Overwrite the entire contents of a Google Doc with new text.

    Args:
        document_id (str): The ID of the document to modify.
        new_content (str): The new text content to insert into the document.
    """
    docs_service = build_docs_service()

    # First, get the current document to determine the number of elements
    doc = docs_service.documents().get(documentId=document_id).execute()
    end_index = doc.get("body", {}).get("content", [])[-1].get("endIndex", 1)

    # Delete all content
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
                "location": {
                    "index": 1
                },
                "text": new_content
            }
        }
    ]

    docs_service.documents().batchUpdate(
        documentId=document_id,
        body={"requests": requests}
    ).execute()
