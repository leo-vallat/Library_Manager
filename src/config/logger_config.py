from datetime import datetime
from logging.handlers import RotatingFileHandler
import logging

log_filename = f"logs/{datetime.now().strftime('%Y%m%d%H%M%S')}.log"

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler(log_filename),  # Écrit dans un fichier
    ]
)

def get_logger(name):
    ''' Return the logger with the name of the calling module '''
    return logging.getLogger(name)