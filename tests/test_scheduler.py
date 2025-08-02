import pytest
from datetime import datetime
from src.scheduler import find_today_task

# Sample schedule rows (mocked as if pulled from Google Sheets)
SAMPLE_ROWS = [
    {
        "Date": "2025-08-01",
        "Pattern Focus": "Sliding Window",
        "Problem Title": "Longest Substring Without Repeating Characters",
        "LeetCode Link": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"
    },
    {
        "Date": "2025-08-02",
        "Pattern Focus": "Sliding Window",
        "Problem Title": "Find All Anagrams in a String",
        "LeetCode Link": "https://leetcode.com/problems/find-all-anagrams-in-a-string/"
    }
]


@pytest.fixture
def fixed_today(monkeypatch):
    """
    Fixture to patch datetime to simulate today's date as 2025-08-01.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest's fixture for dynamically replacing attributes.
    """
    class FixedDate(datetime):
        @classmethod
        def today(cls):
            return cls(2025, 8, 1)

    monkeypatch.setattr("src.scheduler.datetime", FixedDate)


def test_find_today_task_success(fixed_today):
    """
    Test that the correct task is found when today's date is present in the sheet rows.

    Args:
        fixed_today (fixture): Fixture that patches datetime.today() to 2025-08-01.
    """
    result = find_today_task(SAMPLE_ROWS, date_column="Date")
    assert result is not None
    assert result["Problem Title"] == "Longest Substring Without Repeating Characters"


def test_find_today_task_no_match(monkeypatch):
    """
    Test that None is returned when today's date is not in the data.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest fixture used to override datetime.today() with a date not in SAMPLE_ROWS.
    """
    class AltDate(datetime):
        @classmethod
        def today(cls):
            return cls(2025, 8, 10)  # A date not in SAMPLE_ROWS

    monkeypatch.setattr("src.scheduler.datetime", AltDate)

    result = find_today_task(SAMPLE_ROWS, date_column="Date")
    assert result is None


def test_find_today_task_missing_column():
    """
    Test that a KeyError is raised when the date column is missing.
    """
    with pytest.raises(KeyError):
        find_today_task([{"OtherColumn": "2025-08-01"}], date_column="Date")
