import pytest
from src.google_docs import render_template_to_string, create_google_doc, _create_doc_in_drive


@pytest.fixture
def mock_google_services(monkeypatch):
    """
    Mock Google Docs and Drive services.
    """
    captured = {}

    class MockDocsService:
        def documents(self):
            return self
        
        def create(self, body):
            captured["docs_body"] = body
            return self

        def execute(self):
            return {"documentId": "abc123"}
    
    class MockDriveService:
        def files(self):
            return self
        
        def update(self, fileId, addParents, fields):
            captured.update({
                "fileId": fileId,
                "addParents": addParents,
                "fields": fields
            })
            return self
        
        def execute(self):
            return {"id": "abc123"}

    monkeypatch.setattr("src.google_docs.build_docs_service", lambda: MockDocsService())
    monkeypatch.setattr("src.google_docs.build_drive_service", lambda: MockDriveService())

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


def test_create_google_doc_calls_api(monkeypatch, sample_task_row):
    """
    Test that create_google_doc calls the Google Docs API with expected content.

    Args:
        monkeypatch (pytest.MonkeyPatch): Patch external doc creation function.
        sample_task_row (dict): Example task row.
    """
    called = {}

    def mock_create_doc(folder_id, title, content):
        called["folder_id"] = folder_id
        called["title"] = title
        called["content"] = content
        return "mock-doc-id"

    monkeypatch.setattr("src.google_docs._create_doc_in_drive", mock_create_doc)

    blurb = "Focus: {{ pattern_focus }}"
    config = {
        "output_folder_id": "test-folder-id",
        "template_blurb": blurb
    }

    doc_id = create_google_doc(config, sample_task_row)
    assert doc_id == "mock-doc-id"
    assert called["folder_id"] == "test-folder-id"
    assert "Sliding Window" in called["content"]

def test_create_doc_in_drive_calls_apis(mock_google_services):
    """
    Test that _create_doc_in_drive creates a Google Doc and moves it to the
    correct folder.
    """
    captured = mock_google_services
    doc_id = _create_doc_in_drive("folder-xyz", "Test Doc Title", "Some content")

    assert doc_id == "abc123"
    assert captured["docs_body"]["title"] == "Test Doc Title"
    assert captured["fileId"] == "abc123"
    assert captured["addParents"] ==  "folder-xyz"
    assert captured["fields"] == "id"
