import pytest
from datetime import datetime
from src.utils import get_today_str


def test_get_today_str_default(monkeypatch):
    """
    Test get_today_str returns today's date in YYYY-MM-DD format.

    Args:
        monkeypatch (pytest.MonkeyPatch): Used to patch datetime.today()
    """
    class FixedDate(datetime):
        @classmethod
        def today(cls):
            return cls(2025, 8, 1)

    monkeypatch.setattr("src.utils.datetime", FixedDate)

    result = get_today_str()
    assert result == "2025-08-01"
