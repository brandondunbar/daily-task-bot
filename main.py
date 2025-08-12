"""Main entry point for the Daily Task Bot application.

Loads configuration and runs the bot.
"""

from src.config import load_config
from src.constants import BOT_CONFIG_PATH
from src.daily_task_bot import DailyTaskBot


def main():
    """Load configuration and start the Daily Task Bot."""
    config = load_config(BOT_CONFIG_PATH)
    bot = DailyTaskBot(config)
    bot.run()


if __name__ == "__main__":
    main()
