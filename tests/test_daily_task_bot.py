from pathlib import Path
from unittest.mock import patch

import pytest
from src.config_schema import Config, DocBlockConfig, GoogleSheetsConfig
from src.daily_task_bot import DailyTaskBot


@pytest.fixture
def base_sheets_config():
    return GoogleSheetsConfig(
        spreadsheet_id="spreadsheet-id",
        time_zone="UTC",
        date_column_name="Date",
    )


@pytest.fixture(params=[
    ("Block 1", "Sheet1", "templates/t1.md", "doc-1"),
    ("Block X", "TabX", "templates/x.md", "doc-x"),
])
def single_block_config(request, base_sheets_config):
    name, sheet_name, template_path, doc_id = request.param
    return Config(
        google_sheets=base_sheets_config,
        doc_blocks=[
            DocBlockConfig(
                name=name,
                sheet_name=sheet_name,
                template_path=template_path,
                block_title_template="Dummy Title",
                doc_id=doc_id,
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
    """Successfully runs one valid block and updates the target Doc."""
    mock_get_creds.return_value = "creds"
    mock_get_rows.return_value = [
        {"Date": "2025-08-09", "Task Name": "Lesson", "Topic": "X"}
    ]
    task_row = {"Date": "2025-08-09", "Task Name": "Lesson", "Topic": "X"}
    mock_find_today_task.return_value = task_row
    mock_render.return_value = "Rendered Content"

    bot = DailyTaskBot(single_block_config)
    bot.run()

    block = single_block_config.doc_blocks[0]
    mock_get_creds.assert_called_once()
    mock_get_rows.assert_called_once_with(
        sheet_name=block.sheet_name,
        spreadsheet_id="spreadsheet-id",
        credentials="creds"
    )
    mock_find_today_task.assert_called_once_with(
        mock_get_rows.return_value, date_column="Date"
    )
    expected_preprocessed = {"Date": "2025-08-09", "Task_Name": "Lesson", "Topic": "X"}
    mock_render.assert_called_once_with(
        Path(block.template_path), expected_preprocessed)
    mock_overwrite.assert_called_once_with(block.doc_id, "Rendered Content", "creds")


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
    """Concatenates content from multiple enabled blocks sharing one Doc ID."""
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
    mock_overwrite.assert_called_once_with("doc-joined", "Alpha\nBeta", "creds")


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
    """Skips doc update when no task is found for today's date."""
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
def test_run_skips_disabled_block(
    mock_get_creds,
    mock_overwrite,
    disabled_block_config):
    """Skips processing of disabled blocks entirely."""
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


@patch(
        "src.daily_task_bot.get_service_account_credentials",
        side_effect=Exception("Auth failure"))
def test_run_raises_on_credentials_error(mock_get_creds, single_block_config):
    """Raises and logs exception if credentials acquisition fails."""
    with patch("src.daily_task_bot.log.exception") as mock_log:
        bot = DailyTaskBot(single_block_config)
        with pytest.raises(Exception):
            bot.run()
        mock_log.assert_called_once()


@patch("src.daily_task_bot.render_template", side_effect=Exception("Render fail"))
@patch("src.daily_task_bot.find_today_task", return_value={"Date": "2025-08-09"})
@patch("src.daily_task_bot.get_sheet_rows", return_value=[{"Date": "2025-08-09"}])
@patch("src.daily_task_bot.get_service_account_credentials", return_value="creds")
def test_run_raises_on_render_error(
    mock_get_creds, mock_get_rows, mock_find, mock_render, single_block_config
):
    """Logs and raises exception if rendering the template fails."""
    with patch("src.daily_task_bot.log.exception") as mock_log:
        bot = DailyTaskBot(single_block_config)
        with pytest.raises(Exception):
            bot.run()
        mock_log.assert_any_call("content_build_error", error="Render fail")
