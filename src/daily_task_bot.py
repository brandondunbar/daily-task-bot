from src.google_sheets import get_sheet_rows
from src.scheduler import find_today_task
from src.google_docs import overwrite_doc_contents
from src.template import render_template 
from src.auth import get_service_account_credentials


class DailyTaskBot:
    def __init__(self, config):
        self.config = config

    def run(self):
        for block in self.config.doc_blocks:
            if not block.enabled:
                continue

            credentials = get_service_account_credentials()
            
            rows = get_sheet_rows(
                sheet_name=block.sheet_name,
                spreadsheet_id=self.config.google_sheets.spreadsheet_id,
                credentials=credentials
            )

            task = find_today_task(rows, date_column=self.config.google_sheets.date_column_name)

            if not task:
                print(f"No task scheduled for today in block: {block.name}")
                continue

            doc_id = block.doc_id
            new_content = render_template(block.template_path, task)

            overwrite_doc_contents(doc_id, new_content)
