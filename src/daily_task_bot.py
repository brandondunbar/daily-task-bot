from src.google_sheets import get_sheet_rows
from src.scheduler import find_today_task
from src.google_docs import overwrite_doc_contents
from src.template import render_template 
from src.auth import get_service_account_credentials


class DailyTaskBot:
    def __init__(self, config):
        self.config = config

    def run(self):
        credentials = get_service_account_credentials()
        doc_ids = self._get_docs_contents(
            self.config.google_sheets.spreadsheet_id,
            credentials)
        
        for doc_id in doc_ids.keys():
            overwrite_doc_contents(doc_id, doc_ids[doc_id], credentials)
    
    def _get_docs_contents(self, spreadsheet_id, credentials):
        doc_ids = {}
        for block in self.config.doc_blocks:
            if not block.enabled:
                continue

            rows = get_sheet_rows(
                sheet_name=block.sheet_name,
                spreadsheet_id=spreadsheet_id,
                credentials=credentials
            )

            task = find_today_task(rows, date_column=self.config.google_sheets.date_column_name)

            if not task:
                print(f"No task scheduled for today in block: {block.name}")
                continue

            preprocessed_task = {k.replace(" ", "_"): v for k, v in task.items()}
            doc_id = block.doc_id
            new_content = render_template(block.template_path, preprocessed_task)

            if doc_id not in doc_ids.keys():
                doc_ids[doc_id] = new_content
            else:
                doc_ids[doc_id] = doc_ids[doc_id] + new_content
        
        return doc_ids

