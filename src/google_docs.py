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


def create_google_doc(config, row):
    """
    Render content from a template and create a Google Doc in the specified folder.

    Args:
        config (dict): Contains `output_folder_id` and `template_blurb` keys.
        row (dict): A row of task data from the sheet.

    Returns:
        str: The ID of the created Google Doc.
    """
    content = render_template_to_string(config["template_blurb"], row)
    title_template = config.get("title_template", "{{ Date }}")
    title = render_template_to_string(title_template, row)
    folder_id = config["output_folder_id"]
    return _create_doc_in_drive(folder_id, title, content)


def build_docs_service():
    """Return an authenticated Google Docs API service."""
    scopes = ["https://www.googleapis.com/auth/documents"]
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH, scopes=scopes)
    return build("docs", "v1", credentials=creds)


def build_drive_service():
    """Return an authenticated Google Drive API service."""
    scopes = ["https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH, scopes=scopes)
    return build("drive", "v3", credentials=creds)


def _create_doc_in_drive(folder_id, title, content):
    """
    Create a new Google Doc with the given title and content, and move it to the specified folder.

    Args:
        folder_id (str): ID of the target Google Drive folder.
        title (str): Title for the new Google Doc.
        content (str): Body content of the document.

    Returns:
        str: ID of the created document.
    """
    docs_service = build_docs_service()
    drive_service = build_drive_service()

    # Create the document with title and initial content
    doc_metadata = {"title": title}
    doc = docs_service.documents().create(body=doc_metadata).execute()
    doc_id = doc.get("documentId")

    # Move the doc into the specified folder
    drive_service.files().update(
        fileId=doc_id,
        addParents=folder_id,
        fields="id"
    ).execute()

    return doc_id
