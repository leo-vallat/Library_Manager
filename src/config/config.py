from dotenv import load_dotenv
import logging
import os

load_dotenv()

class AppConfig:
    # === ENV VARS === #
    ENV = os.getenv('ENV', 'dev').lower()
    LOG_LEVEL = logging.DEBUG if ENV == 'dev' else logging.INFO
    SHOW_CONSOLE_LOGS = ENV == 'dev'
    DOWNLOADED_MUSIC_FOLDER_PATH = os.getenv('DOWNLOADED_MUSIC_FOLDER_PATH')
    AVAILABLE_FILE_EXTENSION = tuple(os.getenv('AVAILABLE_FILE_EXTENSION'))

    # === STATIC PATHS === #
    ARTWORK_FOLDER_PATH = 'ressources/artwork'
    BATCH_ID_FILE_PATH = 'ressources/batch_id.txt'
    LOGS_FOLDER_PATH = 'logs'

    # === SYSTEM === #
    MUSIC_APP_BUNDLE_ID = 'com.apple.Music'

    @staticmethod
    def validate():
        # Check env vars
        if AppConfig.ENV not in {'dev', 'prod'}:
            raise EnvironmentError(f"ENV must be either 'dev' or 'prod'. Current: '{AppConfig.ENV}'")
        env_vars = {
            'DOWNLOADED_MUSIC_FOLDER_PATH': AppConfig.DOWNLOADED_MUSIC_FOLDER_PATH,
            'AVAILABLE_FILE_EXTENSION': AppConfig.AVAILABLE_FILE_EXTENSION
        }
        missing_vars = [name for name, val in env_vars.items() if not val]
        if missing_vars:
            raise EnvironmentError(f"Missing required env variables in .env : {', '.join(missing_vars)}")
        # Check statis paths
        static_paths = {
            'DOWNLOADED_MUSIC_FOLDER_PATH': AppConfig.DOWNLOADED_MUSIC_FOLDER_PATH,
            'ARTWORK_FOLDER_PATH': AppConfig.ARTWORK_FOLDER_PATH,
            'BATCH_ID_FILE_PATH': AppConfig.BATCH_ID_FILE_PATH,
            'LOGS_FOLDER_PATH': AppConfig.LOGS_FOLDER_PATH
        }        
        missing_paths = [name for name, path in static_paths.items() if not os.path.exists(path)]
        if missing_paths:
            raise EnvironmentError(f"The following paths do not exist : {', '.join(missing_paths)}")
        # Check file extension
        if len(AppConfig.AVAILABLE_FILE_EXTENSION) == 0:
            raise EnvironmentError('AVAILABLE_FILE_EXTENSION is empty in .env')
