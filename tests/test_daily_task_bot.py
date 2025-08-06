import pytest
from unittest.mock import patch, MagicMock
from src.daily_task_bot import DailyTaskBot
from src.config_schema import Config, GoogleSheetsConfig, DocBlockConfig


@pytest.fixture
def dummy_config():
    return Config(
        google_sheets=GoogleSheetsConfig(
            spreadsheet_id="spreadsheet-id",
            time_zone="UTC",
            date_column_name="Date"
        ),
        doc_blocks=[
            DocBlockConfig(
                name="Test Block",
                sheet_name="TestSheet",
                template_path="templates/test_template.md",
                block_title_template="Test - {{ date }}",
                doc_id="test-doc-id",
                enabled=True
            )
        ]
    )


@patch("src.daily_task_bot.get_sheet_rows")
@patch("src.daily_task_bot.find_today_task")
@patch("src.daily_task_bot.render_template")
@patch("src.daily_task_bot.overwrite_doc_contents")
def test_bot_run_with_valid_task(mock_overwrite, mock_render, mock_find_task, mock_get_rows, dummy_config):
    mock_get_rows.return_value = [
        {"Date": "2025-08-06", "Topic": "Test Lesson"}
    ]
    mock_find_task.return_value = {"Date": "2025-08-06", "Topic": "Test Lesson"}
    mock_render.return_value = "Rendered Content"

    bot = DailyTaskBot(dummy_config)
    bot.run()

    mock_get_rows.assert_called_once()
    mock_find_task.assert_called_once()
    mock_render.assert_called_once()
    mock_overwrite.assert_called_once_with("test-doc-id", "Rendered Content")


@patch("src.daily_task_bot.get_sheet_rows")
@patch("src.daily_task_bot.find_today_task")
def test_bot_skips_when_no_task(mock_find_task, mock_get_rows, dummy_config):
    mock_get_rows.return_value = []
    mock_find_task.return_value = None

    bot = DailyTaskBot(dummy_config)
    bot.run()

    mock_get_rows.assert_called_once()
    mock_find_task.assert_called_once()
