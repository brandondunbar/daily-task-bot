"""Main entry point for the Daily Task Bot application.

Initializes logging, loads configuration, and runs the bot.
"""

from src.config import load_config
from src.constants import BOT_CONFIG_PATH
from src.daily_task_bot import DailyTaskBot
from src.observability.logging_setup import configure_logging


def main():
    """Initialize logging, load configuration, and start the bot."""
    # Configure logging once at process startup
    log = configure_logging(service_name="daily-task-bot")

    log.info("application_starting")

    config = load_config(BOT_CONFIG_PATH)
    bot = DailyTaskBot(config)

    try:
        bot.run()
        log.info("application_exited", status="success")
    except Exception as e:
        log.exception("application_exited", status="failure", error=str(e))
        raise


if __name__ == "__main__":
    main()
