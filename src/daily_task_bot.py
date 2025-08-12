"""This module defines the `DailyTaskBot` orchestrator.

Coordinates the daily task workflow: reads tasks from Google Sheets,
renders template content, and updates Google Docs accordingly.
"""

from src.auth import get_service_account_credentials
from src.google_docs import overwrite_doc_contents
from src.google_sheets import get_sheet_rows
from src.scheduler import find_today_task
from src.template import render_template


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
        credentials = get_service_account_credentials()
        doc_ids = self._get_docs_contents(
            self.config.google_sheets.spreadsheet_id,
            credentials)

        for doc_id in doc_ids.keys():
            overwrite_doc_contents(doc_id, doc_ids[doc_id], credentials)

    def _get_docs_contents(self, spreadsheet_id, credentials):
        """Build a mapping of Google Doc IDs to rendered content.

        Iterates over configured document blocks, fetches today's task from
        the corresponding sheet tab, preprocesses the row keys, renders the
        template, and aggregates content per destination Doc.

        Args:
            spreadsheet_id: The Google Sheets spreadsheet ID to read from.
            credentials: Authenticated Google credentials used for API calls.

        Returns:
            A mapping from destination Google Doc ID to the full rendered content
            that should be written to that document.
        """
        doc_ids = {}
        for block in self.config.doc_blocks:
            if not block.enabled:
                continue

            rows = get_sheet_rows(
                sheet_name=block.sheet_name,
                spreadsheet_id=spreadsheet_id,
                credentials=credentials
            )

            task = find_today_task(
                rows, date_column=self.config.google_sheets.date_column_name)

            if not task:
                print(f"No task scheduled for today in block: {block.name}")
                continue

            preprocessed_task = {k.replace(" ", "_"): v for k, v in task.items()}
            doc_id = block.doc_id
            new_content = render_template(block.template_path, preprocessed_task)

            if doc_id not in doc_ids.keys():
                doc_ids[doc_id] = new_content
            else:
                doc_ids[doc_id] = doc_ids[doc_id] + "\n" + new_content

        return doc_ids

