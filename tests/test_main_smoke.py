import pytest
from src.main import main

mock_config = {
    "sheets": [{
        "name": "Mock Sheet",
        "id": "fake-id",
        "worksheet": "Sheet1",
        "date_column": "date",
        "output_folder_id": "folder123",
        "template_blurb": "Focus: {{ pattern_focus }}",
        "title_template": "{{ pattern_focus }}",
        "column_mapping": {
            "pattern_focus": "Pattern Focus",
            "problem_title": "Problem Title",
            "leetcode_link": "LeetCode Link",
            "date": "Date"
        }
    }],
    "calendar": {
        "title_template": "{{ pattern_focus }}",
        "time": "08:00",
        "duration_minutes": 45
    }
}

mock_rows = [
    {
        "pattern_focus": "Sliding Window",
        "problem_title": "Longest Substring Without Repeating Characters",
        "leetcode_link": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
        "date": "2025-08-01"
    }
]

mock_row = mock_rows[0]


def test_main_smoke(monkeypatch):
    """
    Smoke test for main.py to confirm the integration flow executes without errors.

    Args:
        monkeypatch (pytest.MonkeyPatch): Used to mock all submodule functions.
    """
    monkeypatch.setattr("src.main.load_config", lambda path: mock_config)
    monkeypatch.setattr("src.main.get_sheet_rows", lambda conf, creds: mock_rows)
    monkeypatch.setattr("src.main.find_today_task", lambda rows, date_column: mock_row)
    monkeypatch.setattr("src.main.create_google_doc", lambda conf, row: "mock-doc-link")
    monkeypatch.setattr("src.main.create_calendar_event", lambda conf, row, doc: "mock-event-id")

    # Should run without exceptions
    main()
