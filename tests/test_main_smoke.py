from pathlib import Path
from unittest.mock import patch

import pytest  # noqa: F401
from src.config_schema import Config, DocBlockConfig, GoogleSheetsConfig
from src.daily_task_bot import DailyTaskBot


def test_main_smoke_with_daily_task_bot():
    """End-to-end smoke test: DailyTaskBot runs without errors and writes a doc."""

    # Build a minimal but valid config using the new schema
    cfg = Config(
        google_sheets=GoogleSheetsConfig(
            spreadsheet_id="spreadsheet-id",
            time_zone="UTC",
            date_column_name="Date",
        ),
        doc_blocks=[
            DocBlockConfig(
                name="Smoke Block",
                sheet_name="Sheet1",
                template_path="templates/smoke.md",
                block_title_template="Smoke {{ Date }}",
                doc_id="doc-smoke",
                enabled=True,
            )
        ],
    )
    PATCH_CREDS = "src.daily_task_bot.get_service_account_credentials"
    PATCH_ROWS = "src.daily_task_bot.get_sheet_rows"
    PATCH_FIND = "src.daily_task_bot.find_today_task"
    PATCH_RENDER = "src.daily_task_bot.render_template"
    PATCH_WRITE = "src.daily_task_bot.overwrite_doc_contents"

    with (
        patch(PATCH_CREDS, return_value="creds") as mock_creds,
        patch(PATCH_ROWS,
              return_value=[{"Date": "2025-08-01", "Task": "X"}]) as mock_rows,
        patch(PATCH_FIND,
              return_value={"Date": "2025-08-01", "Task": "X"}) as mock_find,
        patch(PATCH_RENDER, return_value="Rendered Smoke") as mock_render,
        patch(PATCH_WRITE) as mock_write,
    ):

        bot = DailyTaskBot(cfg)
        bot.run()

        mock_creds.assert_called_once()
        mock_rows.assert_called_once_with(
            sheet_name="Sheet1",
            spreadsheet_id="spreadsheet-id",
            credentials="creds",
        )
        mock_find.assert_called_once_with(
            [{"Date": "2025-08-01", "Task": "X"}], date_column="Date")
        # render_template receives a Path and the preprocessed dict(spaces->underscores)
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        assert isinstance(args[0], Path)
        assert "Date" in args[1] and "Task" in args[1]
        mock_write.assert_called_once_with("doc-smoke", "Rendered Smoke", "creds")
