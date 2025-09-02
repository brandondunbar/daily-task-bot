"""Main entry point for the Daily Task Bot application.

Initializes logging, loads configuration, and runs the bot with graceful shutdown.
"""

import signal
import threading
from typing import Callable

from src.config import load_config
from src.constants import BOT_CONFIG_PATH
from src.daily_task_bot import DailyTaskBot
from src.observability.logging_setup import configure_logging

# Global shutdown event that signal handlers can set
_shutdown_event = threading.Event()


def _maybe_call(method: Callable, log) -> None:
    """Call a method safely for shutdown/cleanup and log exceptions."""
    try:
        method()
    except Exception as e:  # noqa: BLE001 - best effort during shutdown
        if log:
            log.exception("shutdown_hook_error", error=str(e))


def _install_signal_handlers(bot: DailyTaskBot, log) -> None:
    """Install SIGINT/SIGTERM handlers that request an orderly shutdown.

    The handler will try common method names on your bot in this order:
    `stop()`, `shutdown()`, `close()`, `cancel()`.
    If none exist, it simply sets the global shutdown event. Your bot can
    optionally poll `is_shutting_down()` if you wire that in.
    """

    def handler(signum, frame):  # noqa: ARG001 - signature required by signal
        if log:
            log.info("signal_received", signum=signum)
        _shutdown_event.set()

        # Best-effort: ask the bot to stop if it exposes a conventional API
        for name in ("stop", "shutdown", "close", "cancel"):
            if hasattr(bot, name) and callable(getattr(bot, name)):
                if log:
                    log.info("invoking_shutdown_hook", method=name)
                _maybe_call(getattr(bot, name), log)
                break

    # Register for Ctrl+C and `docker stop`
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)


def is_shutting_down() -> bool:
    """Expose shutdown intent (optional for your bot to poll)."""
    return _shutdown_event.is_set()


def main():
    """Initialize logging, load configuration, and start the bot."""
    # Configure logging once at process startup
    log = configure_logging(service_name="daily-task-bot")
    log.info("application_starting")

    config = load_config(BOT_CONFIG_PATH)
    bot = DailyTaskBot(config)

    # Wire signal handlers so `docker stop` triggers a clean exit
    _install_signal_handlers(bot, log)

    try:
        # If your bot supports a cooperative loop, it can poll `is_shutting_down()`.
        # Otherwise, the signal handler above will try to call bot.stop()/shutdown().
        bot.run()
        log.info("application_exited", status="success")
    except Exception as e:
        log.exception("application_exited", status="failure", error=str(e))
        raise
    finally:
        # Final best-effort cleanup hook if present
        for name in ("cleanup", "close"):
            if hasattr(bot, name) and callable(getattr(bot, name)):
                _maybe_call(getattr(bot, name), log)
        log.info("application_cleanup_complete")


if __name__ == "__main__":
    main()
