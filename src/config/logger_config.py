from datetime import datetime
from src.config.config import AppConfig
from logging.handlers import RotatingFileHandler
import logging
import os

LOGS_FOLDER_PATH = AppConfig.LOGS_FOLDER_PATH

log_filename = os.path.join(LOGS_FOLDER_PATH, f"app_{AppConfig.ENV}.log")
log_level = logging.INFO if AppConfig.ENV == 'prod' else logging.DEBUG

def get_logger(name):
    ''' Return the logger with the name of the calling module '''
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
    ''' Log a visual session delimiter in the log '''
    session_time = datetime.now().strftime('%Y:%m:%d %H:%M:%S')
    logger.info('=' * 60)
    logger.info(f"📀 Nouvelle session - {session_time}")
    logger.info('=' * 60)
