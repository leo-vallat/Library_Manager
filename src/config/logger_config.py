from datetime import datetime
from src.config.config import AppConfig
from logging.handlers import RotatingFileHandler
import logging
import os

LOGS_FOLDER_PATH = AppConfig.LOGS_FOLDER_PATH

log_filename = os.path.join(LOGS_FOLDER_PATH, f"app_{AppConfig.ENV}.log")
log_level = logging.INFO if AppConfig.ENV == 'prod' else logging.DEBUG

def get_logger(name):
    """
    Returns a logger instance configured for the application.

    - Logs messages to a rotating file handler.
    - Optionally logs messages to the console if enabled in the configuration.

    Args:
        name (str): The name of the logger, typically the calling module's name.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    if not logger.hasHandlers():
        file_formatter = logging.Formatter('%(levelname)s:%(name)s : %(message)s')
        file_handler = RotatingFileHandler(log_filename, maxBytes=1_000_000, backupCount=5)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        if AppConfig.SHOW_CONSOLE_LOGS:
            console_formatter = logging.Formatter('%(levelname)s - %(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
    return logger

def log_session_start(logger):
    """
    Logs a visual delimiter to indicate the start of a new session.

    - Includes a timestamp for the session start.

    Args:
        logger (logging.Logger): The logger instance to log the session start.
    """
    session_time = datetime.now().strftime('%Y:%m:%d %H:%M:%S')
    logger.info('=' * 60)
    logger.info(f"🟢 New Session - {session_time}")
    logger.info('=' * 60)
