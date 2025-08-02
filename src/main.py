from src.config_loader import load_config
from src.google_sheets import get_sheet_rows
from src.scheduler import find_today_task
from src.google_docs import create_google_doc
from src.google_calendar import create_calendar_event


def main():
    config = load_config("config.yaml")
    sheet_conf = config["sheets"][0]  # MVP; one sheet only

    rows = get_sheet_rows(sheet_conf, credentials={})
    task = find_today_task(rows, date_column=sheet_conf["date_column"])

    if not task:
        print("No task scheduled for today.")
        return

    doc_link = create_google_doc(sheet_conf, task)
    create_calendar_event(config, task, doc_link)


if __name__ == "__main__":
    main()
