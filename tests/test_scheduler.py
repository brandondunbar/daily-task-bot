from unittest.mock import patch

import pytest
from src.scheduler import find_today_task

# Sample schedule rows (mocked as if pulled from Google Sheets)
SAMPLE_ROWS = [
    {
        "Date": "2025-08-01",
        "Pattern Focus": "Sliding Window",
        "Problem Title": "Longest Substring Without Repeating Characters",
        "LeetCode Link": "https://leetcode.com/problems/lrs/"
    },
    {
        "Date": "2025-08-02",
        "Pattern Focus": "Sliding Window",
        "Problem Title": "Find All Anagrams in a String",
        "LeetCode Link": "https://leetcode.com/problems/fng/"
    }
]


@pytest.mark.parametrize(
    "today,rows,date_column,expected",
    [
        ("2025-08-01", SAMPLE_ROWS, "Date", SAMPLE_ROWS[0]),
        ("2025-08-10", SAMPLE_ROWS, "Date", None),
        ("2025-08-01", [
            {"Date": "2025-08-01"},
            {"Date": "2025-08-01"}],
            "Date", {"Date": "2025-08-01"}),
        ("2025-08-01", [
            {"Scheduled Date": "2025-08-01", "Problem Title": "Custom Col"}],
            "Scheduled Date", {
                "Scheduled Date": "2025-08-01",
                "Problem Title": "Custom Col"}),
        ("2025-08-01", [], "Date", None),
        ("2025-08-01", [{"Date": "2025/08/01"}], "Date", None),
    ]
)
def test_find_today_task_param(monkeypatch, today, rows, date_column, expected):
    """Returns correct row or None based on today's date and column name."""
    monkeypatch.setattr("src.scheduler.get_today_str", lambda: today)
    result = find_today_task(rows, date_column=date_column)
    assert result == expected


def test_find_today_task_missing_column():
    """Raises KeyError if required date column is missing from input rows."""
    with pytest.raises(KeyError):
        find_today_task([{"OtherColumn": "2025-08-01"}], date_column="Date")


def test_column_name_case_sensitivity(monkeypatch):
    """Ensures column name is case-sensitive and raises KeyError if mismatched."""
    monkeypatch.setattr("src.scheduler.get_today_str", lambda: "2025-08-01")
    rows = [{"date": "2025-08-01"}]
    with pytest.raises(KeyError):
        find_today_task(rows, date_column="Date")


def test_logging_on_successful_match(monkeypatch):
    """Emits 'today_task_found' log when a matching row is found."""
    monkeypatch.setattr("src.scheduler.get_today_str", lambda: "2025-08-01")
    with patch("src.scheduler.log.info") as mock_info:
        result = find_today_task(SAMPLE_ROWS)
        assert result is not None
        mock_info.assert_any_call("today_task_found", row_index=0)


def test_logging_when_not_found(monkeypatch):
    """Emits 'today_task_not_found' log when no matching row exists."""
    monkeypatch.setattr("src.scheduler.get_today_str", lambda: "2025-08-10")
    with patch("src.scheduler.log.info") as mock_info:
        result = find_today_task(SAMPLE_ROWS)
        assert result is None
        mock_info.assert_any_call("today_task_not_found")


def test_logging_on_missing_column():
    """Logs an exception and raises KeyError when date column is missing."""
    rows = [{"NotDate": "2025-08-01"}]
    with patch("src.scheduler.log.exception") as mock_exception:
        with pytest.raises(KeyError):
            find_today_task(rows)
        mock_exception.assert_called_once()
