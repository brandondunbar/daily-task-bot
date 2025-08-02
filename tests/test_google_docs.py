import pytest
from src.google_docs import render_template_to_string, create_google_doc


@pytest.fixture
def sample_task_row():
    return {
        "Pattern Focus": "Sliding Window",
        "Problem Title": "Longest Substring Without Repeating Characters",
        "LeetCode Link": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"
    }


@pytest.fixture
def sample_blurb():
    return "Today's focus is on {{ Pattern Focus }}. Solve: {{ Problem Title }} - {{ LeetCode Link }}"


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

    blurb = "Focus: {{ Pattern Focus }}"
    config = {
        "output_folder_id": "test-folder-id",
        "template_blurb": blurb
    }

    doc_id = create_google_doc(config, sample_task_row)
    assert doc_id == "mock-doc-id"
    assert called["folder_id"] == "test-folder-id"
    assert "Sliding Window" in called["content"]
