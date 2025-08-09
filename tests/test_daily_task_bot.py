import pytest
from unittest.mock import patch
from src.daily_task_bot import DailyTaskBot
from src.config_schema import Config, GoogleSheetsConfig, DocBlockConfig
from pathlib import Path


@pytest.fixture
def base_sheets_config():
    return GoogleSheetsConfig(
        spreadsheet_id="spreadsheet-id",
        time_zone="UTC",
        date_column_name="Date",
    )


@pytest.fixture
def single_block_config(base_sheets_config):
    return Config(
        google_sheets=base_sheets_config,
        doc_blocks=[
            DocBlockConfig(
                name="Block 1",
                sheet_name="Sheet1",
                template_path="templates/t1.md",
                block_title_template="Dummy Title",
                doc_id="doc-1",
                enabled=True,
            )
        ],
    )


@pytest.fixture
def two_blocks_same_doc_config(base_sheets_config):
    return Config(
        google_sheets=base_sheets_config,
        doc_blocks=[
            DocBlockConfig(
                name="Block A",
                sheet_name="SheetA",
                template_path="templates/a.md",
                block_title_template="Dummy Title",
                doc_id="doc-joined",
                enabled=True,
            ),
            DocBlockConfig(
                name="Block B",
                sheet_name="SheetB",
                template_path="templates/b.md",
                block_title_template="Dummy Title",
                doc_id="doc-joined",
                enabled=True,
            ),
        ],
    )


@pytest.fixture
def disabled_block_config(base_sheets_config):
    return Config(
        google_sheets=base_sheets_config,
        doc_blocks=[
            DocBlockConfig(
                name="Disabled Block",
                sheet_name="ShouldNotCall",
                template_path="templates/skip.md",
                block_title_template="Dummy Title",
                doc_id="doc-skip",
                enabled=False,
            )
        ],
    )


@patch("src.daily_task_bot.overwrite_doc_contents")
@patch("src.daily_task_bot.render_template")
@patch("src.daily_task_bot.find_today_task")
@patch("src.daily_task_bot.get_sheet_rows")
@patch("src.daily_task_bot.get_service_account_credentials")
def test_run_single_block_valid_task(
    mock_get_creds,
    mock_get_rows,
    mock_find_today_task,
    mock_render,
    mock_overwrite,
    single_block_config,
):
    mock_get_creds.return_value = "creds"
    mock_get_rows.return_value = [
        {"Date": "2025-08-09", "Task Name": "Lesson", "Topic": "X"}
    ]
    task_row = {"Date": "2025-08-09", "Task Name": "Lesson", "Topic": "X"}
    mock_find_today_task.return_value = task_row
    mock_render.return_value = "Rendered Content"

    bot = DailyTaskBot(single_block_config)
    bot.run()

    mock_get_creds.assert_called_once()
    mock_get_rows.assert_called_once_with(
        sheet_name="Sheet1", spreadsheet_id="spreadsheet-id", credentials="creds"
    )
    mock_find_today_task.assert_called_once_with(
        mock_get_rows.return_value, date_column="Date"
    )
    expected_preprocessed = {"Date": "2025-08-09", "Task_Name": "Lesson", "Topic": "X"}
    mock_render.assert_called_once_with(Path("templates/t1.md"), expected_preprocessed)
    mock_overwrite.assert_called_once_with("doc-1", "Rendered Content", "creds")


@patch("src.daily_task_bot.overwrite_doc_contents")
@patch("src.daily_task_bot.render_template")
@patch("src.daily_task_bot.find_today_task")
@patch("src.daily_task_bot.get_sheet_rows")
@patch("src.daily_task_bot.get_service_account_credentials")
def test_run_concatenates_multiple_blocks_same_doc(
    mock_get_creds,
    mock_get_rows,
    mock_find_today_task,
    mock_render,
    mock_overwrite,
    two_blocks_same_doc_config,
):
    mock_get_creds.return_value = "creds"
    mock_get_rows.side_effect = [
        [{"Date": "2025-08-09", "Item": "A"}],
        [{"Date": "2025-08-09", "Item": "B"}],
    ]
    mock_find_today_task.side_effect = [
        {"Date": "2025-08-09", "Item": "A"},
        {"Date": "2025-08-09", "Item": "B"},
    ]
    mock_render.side_effect = ["Alpha", "Beta"]

    bot = DailyTaskBot(two_blocks_same_doc_config)
    bot.run()

    assert mock_render.call_count == 2
    mock_overwrite.assert_called_once_with("doc-joined", "AlphaBeta", "creds")


@patch("src.daily_task_bot.overwrite_doc_contents")
@patch("src.daily_task_bot.render_template")
@patch("src.daily_task_bot.find_today_task")
@patch("src.daily_task_bot.get_sheet_rows")
@patch("src.daily_task_bot.get_service_account_credentials")
def test_run_skips_when_no_task(
    mock_get_creds,
    mock_get_rows,
    mock_find_today_task,
    mock_render,
    mock_overwrite,
    single_block_config,
):
    mock_get_creds.return_value = "creds"
    mock_get_rows.return_value = []
    mock_find_today_task.return_value = None

    bot = DailyTaskBot(single_block_config)
    bot.run()

    mock_get_rows.assert_called_once()
    mock_find_today_task.assert_called_once()
    mock_render.assert_not_called()
    mock_overwrite.assert_not_called()


@patch("src.daily_task_bot.overwrite_doc_contents")
@patch("src.daily_task_bot.get_service_account_credentials")
def test_run_skips_disabled_block(mock_get_creds, mock_overwrite, disabled_block_config):
    mock_get_creds.return_value = "creds"

    bot = DailyTaskBot(disabled_block_config)

    with patch("src.daily_task_bot.get_sheet_rows") as mock_get_rows, \
         patch("src.daily_task_bot.find_today_task") as mock_find_task, \
         patch("src.daily_task_bot.render_template") as mock_render:
        bot.run()
        mock_get_rows.assert_not_called()
        mock_find_task.assert_not_called()
        mock_render.assert_not_called()

    mock_overwrite.assert_not_called()
