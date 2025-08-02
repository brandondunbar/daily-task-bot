import pytest
from src.google_calendar import create_calendar_event


def test_create_calendar_event_payload(monkeypatch):
    """
    Test that create_calendar_event constructs a valid calendar event payload and
    calls the underlying calendar API with the correct parameters.

    Args:
        monkeypatch (pytest.MonkeyPatch): Used to patch the actual calendar API call.
    """
    captured = {}

    def mock_create_event_on_calendar(summary, time, duration, description, doc_link):
        captured["summary"] = summary
        captured["time"] = time
        captured["duration"] = duration
        captured["description"] = description
        captured["doc_link"] = doc_link
        return "mock-event-id"

    monkeypatch.setattr("src.google_calendar._create_event_on_calendar", mock_create_event_on_calendar)

    config = {
        "calendar": {
            "title_template": "{{ pattern_focus }}",
            "time": "09:00",
            "duration_minutes": 45
        }
    }

    row = {
        "pattern_focus": "Sliding Window",
        "problem_title": "Longest Substring Without Repeating Characters",
        "leetcode_link": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
        "Date": "2025-08-01"
    }

    doc_link = "https://docs.google.com/document/d/mock"

    event_id = create_calendar_event(config, row, doc_link)

    assert event_id == "mock-event-id"
    assert captured["summary"] == "Sliding Window"
    assert captured["time"] == "09:00"
    assert captured["duration"] == 45
    assert "Longest Substring Without Repeating Characters" in captured["description"]
    assert doc_link in captured["doc_link"]
