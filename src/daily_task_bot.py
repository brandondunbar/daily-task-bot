"""This module defines the `DailyTaskBot` orchestrator.

Coordinates the daily task workflow: reads tasks from Google Sheets,
renders template content, and updates Google Docs accordingly.
"""

from src.auth import get_service_account_credentials
from src.google_docs import overwrite_doc_contents
from src.google_sheets import get_sheet_rows
from src.observability.logging_setup import get_logger
from src.scheduler import find_today_task
from src.template import render_template

log = get_logger(__name__)


class DailyTaskBot:
    """Orchestrates pulling tasks from Sheets and writing content to Docs.

    Attributes:
        config: Application configuration object containing Google Sheets
            settings and a list of document-generation blocks to process.
    """

    def __init__(self, config):  # noqa: D107
        self.config = config

    def run(self):
        """Execute the end-to-end task pipeline for all enabled blocks.

        Steps:
            1. Acquire Google service account credentials.
            2. Gather rendered content for each destination Doc.
            3. Overwrite each target Doc with the new content.
        """
        log.info(
            "run_started",
            blocks=len(getattr(self.config, "doc_blocks", []) or []),
            spreadsheet_id=self.config.google_sheets.spreadsheet_id,
        )

        try:
            credentials = get_service_account_credentials()
        except Exception as e:
            log.exception("credentials_error", error=str(e))
            raise

        try:
            doc_contents = self._get_docs_contents(
                self.config.google_sheets.spreadsheet_id, credentials
            )
        except Exception as e:
            log.exception("content_build_error", error=str(e))
            raise

        updated, failed = 0, 0
        for doc_id, content in doc_contents.items():
            try:
                overwrite_doc_contents(doc_id, content, credentials)
                updated += 1
                log.info("doc_updated", doc_id=doc_id)
            except Exception as e:
                failed += 1
                log.exception("doc_update_failed", doc_id=doc_id, error=str(e))

        log.info("run_completed", docs_updated=updated, docs_failed=failed)

    def _get_docs_contents(self, spreadsheet_id, credentials):
        """Build a mapping of Google Doc IDs to rendered content.

        Iterates over configured document blocks, fetches today's task from the
        corresponding sheet tab, preprocesses the row keys, renders the
        template, and aggregates content per destination Doc.

        Args:
            spreadsheet_id: The Google Sheets spreadsheet ID to read from.
            credentials: Authenticated Google credentials used for API calls.

        Returns:
            A mapping from destination Google Doc ID to the full rendered
            content that should be written to that document.
        """
        doc_ids: dict[str, str] = {}

        for block in self.config.doc_blocks:
            if not block.enabled:
                log.info("block_skipped_disabled", block=block.name)
                continue

            log.info("block_processing", block=block.name, sheet=block.sheet_name)

            rows = get_sheet_rows(
                sheet_name=block.sheet_name,
                spreadsheet_id=spreadsheet_id,
                credentials=credentials,
            )

            task = find_today_task(
                rows, date_column=self.config.google_sheets.date_column_name
            )

            if not task:
                log.info("no_task_today", block=block.name)
                continue

            preprocessed_task = {k.replace(" ", "_"): v for k, v in task.items()}
            new_content = render_template(block.template_path, preprocessed_task)

            if block.doc_id not in doc_ids:
                doc_ids[block.doc_id] = new_content
            else:
                doc_ids[block.doc_id] = doc_ids[block.doc_id] + "\n" + new_content

        return doc_ids
