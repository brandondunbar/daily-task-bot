import pytest
from src.google_docs import render_template_to_string, edit_title, overwrite_doc_contents


@pytest.fixture
def mock_google_docs_service(monkeypatch):
    """
    Mock Google Docs service.
    """
    captured = {"requests": []}

    class MockDocuments:
        def get(self, documentId):
            return self

        def execute(self):
            return {
                "body": {
                    "content": [
                        {"endIndex": 25}
                    ]
                }
            }

        def update(self, documentId, body):
            captured["title_update"] = (documentId, body)
            return self

        def batchUpdate(self, documentId, body):
            captured["batch_update"] = (documentId, body)
            return self

    class MockDocsService:
        def documents(self):
            return MockDocuments()

    monkeypatch.setattr("src.google_docs.build_docs_service", lambda: MockDocsService())
    return captured


@pytest.fixture
def sample_task_row():
    return {
        "pattern_focus": "Sliding Window",
        "problem_title": "Longest Substring Without Repeating Characters",
        "leetcode_link": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"
    }


@pytest.fixture
def sample_blurb():
    return "Today's focus is on {{ pattern_focus }}. Solve: {{ problem_title }} - {{ leetcode_link }}"


def test_render_template_to_string_fills_blurb(sample_task_row, sample_blurb):
    """
    Test that a template blurb is correctly rendered with task row data.

    Args:
        sample_task_row (dict): Simulated row of task data.
        sample_blurb (str): Template with placeholders.
    """
    rendered = render_template_to_string(sample_blurb, sample_task_row) 
    assert "Sliding Window" in rendered
    assert "Longest Substring Without Repeating Characters" in rendered
    assert "https://leetcode.com/problems/longest-substring-without-repeating-characters/" in rendered


def test_edit_title(mock_google_docs_service):
    """
    Test that edit_title sends the correct document ID and title update payload
    to the Google Docs API.
    """
    edit_title("abc123", "New Title")
    doc_id, body = mock_google_docs_service["title_update"]
    assert doc_id == "abc123"
    assert body["title"] == "New Title"


def test_overwrite_doc_contents(mock_google_docs_service):
    """
    Test that overwrite_doc_contents deletes existing content and inserts
    the new content at the start of the document.
    """
    overwrite_doc_contents("abc123", "Overwritten content.")
    doc_id, body = mock_google_docs_service["batch_update"]
    assert doc_id == "abc123"

    requests = body["requests"]
    assert requests[0]["deleteContentRange"]["range"] == {"startIndex": 1, "endIndex": 24}
    assert requests[1]["insertText"] == {"location": {"index": 1}, "text": "Overwritten content."}
