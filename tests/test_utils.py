from datetime import datetime

import pytest
from src.utils import get_today_str


def test_get_today_str_default(monkeypatch):
    """Returns today's date in default YYYY-MM-DD format."""
    class FixedDate(datetime):
        @classmethod
        def today(cls):
            return cls(2025, 8, 1)

    monkeypatch.setattr("src.utils.datetime", FixedDate)

    result = get_today_str()
    assert result == "2025-08-01"


@pytest.mark.parametrize("fmt, expected", [
    ("%d/%m/%Y", "01/08/2025"),
    ("%B %d, %Y", "August 01, 2025"),
    ("%Y%m%d", "20250801"),
])
def test_get_today_str_custom_formats(monkeypatch, fmt, expected):
    """Returns today's date in various custom formats."""
    class FixedDate(datetime):
        @classmethod
        def today(cls):
            return cls(2025, 8, 1)

    monkeypatch.setattr("src.utils.datetime", FixedDate)
    result = get_today_str(fmt=fmt)
    assert result == expected


def test_get_today_str_invalid_format(monkeypatch):
    """Falls back to literal text for an unknown directive (strftime behavior)."""
    class FixedDate(datetime):
        @classmethod
        def today(cls):
            return cls(2025, 8, 1)

    monkeypatch.setattr("src.utils.datetime", FixedDate)

    result = get_today_str(fmt="%Q")
    assert result == "%Q"

