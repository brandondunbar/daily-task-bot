from src.config import load_config
from src.constants import CONFIG_PATH
from src.daily_task_bot import DailyTaskBot


def main():
    config = load_config(CONFIG_PATH)
    bot = DailyTaskBot(config)
    bot.run()


if __name__ == "__main__":
    main()
