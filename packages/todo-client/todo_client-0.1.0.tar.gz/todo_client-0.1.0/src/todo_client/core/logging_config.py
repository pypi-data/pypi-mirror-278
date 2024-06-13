import logging
import logging.config
import os

from datetime import datetime

DEFAULT_FILE_PREFIX = "app"
DEFAULT_LOG_DIR = "log"
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logging(
    default_level=logging.INFO,
    log_dir=DEFAULT_LOG_DIR,
    log_file_prefix=DEFAULT_FILE_PREFIX,
    log_format=DEFAULT_LOG_FORMAT,
):
    """
    Set up logging for the application.

    This function configures two log handlers: one for writing logs to a file, and one for writing logs to the console.
    The log file is created in the specified directory, with a name based on the current date.

    :param default_level: The default logging level.
    :type default_level: int
    :param log_dir: The directory where the log file will be created.
    :type log_dir: str
    :param log_file_prefix: The prefix for the log file name.
    :type log_file_prefix: str
    :param log_format: The format for the log messages.
    :type log_format: str
    """
    # Ensure the logs directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Set the log file name with the current date
    today = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f"{log_file_prefix}-{today}.log")

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": log_format, "datefmt": "%Y-%m-%d %H:%M:%S"}
        },
        "handlers": {
            "file_handler": {
                "level": default_level,
                "formatter": "standard",
                "class": "logging.FileHandler",
                "filename": log_file,
            },
            "console_handler": {
                "level": logging.WARNING,
                "formatter": "standard",
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["file_handler", "console_handler"],
            "level": default_level,
        },
    }

    logging.config.dictConfig(logging_config)
