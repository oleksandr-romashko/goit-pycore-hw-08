"""
Logging configuration module.

Provides a utility function to initialize basic logging for the application,
including log level and message format.

Usage:
    from log_config import init_logging

    init_logging(logging.DEBUG)  # Or any desired level

By default, logs are output to the console (stderr). For production use or
debugging purposes, consider redirecting logs to a file.
"""
import logging


def init_logging(level: int = logging.INFO, log_file: str = "app.log"):
    """
    Sets up basic logging configuration for the application.

    Logs are output to both the console (stderr) and a file.

    Args:
        level (int): Logging level for console output (e.g., logging.DEBUG, logging.INFO).
        log_file (str): Path to the log file. Defaults to 'app.log'.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),  # Console output
            logging.FileHandler(log_file, mode="a", encoding="utf-8"),  # File output
        ],
    )
