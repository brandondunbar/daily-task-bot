"""Logging configuration for the Daily Task Bot.

Provides helpers to configure structured JSON logging with structlog and
stdlib logging. Designed to emit logs to stdout so they can be collected
by container platforms like Kubernetes/GKE.

Usage:
    In your main entrypoint (e.g., main.py):

        from src.observability import logging_setup

        def main():
            log = logging_setup.configure_logging(service_name="daily-task-bot")
            log.info("application_starting")
            # ...
            log.info("application_exited")

    In other modules:

        from src.observability.logging_setup import get_logger

        log = get_logger(__name__)
        log.info("some_event", key="value")
"""

import logging
import os
import sys

import structlog


def _level_from_env(default: str = "INFO") -> str:
    """Read the desired log level from the LOG_LEVEL environment variable.

    Args:
        default: Fallback level if LOG_LEVEL is not set.

    Returns:
        A log level string (e.g., "INFO", "DEBUG").
    """
    return os.getenv("LOG_LEVEL", default).upper()


def configure_logging(service_name: str = "daily-task-bot"):
    """Set up structured logging for the application.

    Configures both the Python stdlib logger and structlog to output
    single-line JSON to stdout. This should be called once at process
    startup, typically from main.py.

    Args:
        service_name: Value to attach to log entries identifying the service.

    Returns:
        A structlog logger pre-bound with the service name.
    """
    # Route stdlib logs to stdout with a simple formatter (message only).
    logging.basicConfig(
        level=_level_from_env(),
        format="%(message)s",
        stream=sys.stdout,
    )

    # Reduce noise from common third-party libraries.
    for noisy in ("uvicorn", "urllib3", "botocore", "google", "asyncio"):
        logging.getLogger(noisy).setLevel(os.getenv("NOISY_LOG_LEVEL", "WARNING"))

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,  # include bound contextvars
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, _level_from_env())
        ),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger().bind(service=service_name)


def get_logger(name: str | None = None):
    """Return a structlog logger for the given name.

    Useful for getting a module-scoped logger without reconfiguring
    logging.

    Args:
        name: Optional logger name (defaults to a generic structlog logger).

    Returns:
        A structlog logger.
    """
    return structlog.get_logger(name)
