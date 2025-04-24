from src.config.config import AppConfig
from src.config.logger_config import get_logger

class Batch:    
    def __init__(self, batch_id : int):
        self.logger = get_logger(self.__class__.__name__)
        self.id = batch_id
        self.tracks = {} 
        self.logger.debug(f"New batch started (ID={self.id})")

    @classmethod
    def new(cls):
        ''' Create a new batch with an auto-incremented ID '''
        batch_id = cls.get_new_id()
        return cls(batch_id)
    
    @classmethod
    def from_current_id(cls):
        ''' Load the last added batch '''
        batch_id = cls.get_current_id()
        return cls(batch_id)
    
    @classmethod
    def from_existing_id(cls, batch_id : int):
        ''' Load an existing batch '''
        return cls(batch_id)

    @staticmethod
    def get_new_id():
        logger = get_logger(__name__)
        path = AppConfig.BATCH_ID_FILE_PATH

        with open(path, 'r') as f:
            try:
                batch_id = int(f.read().strip())
            except ValueError:
                logger.error("❌ Invalid value found in batch_id.txt. Please fix manually.")
                raise ValueError("Invalid batch_id.txt value — expected integer.")
        batch_id += 1

        with open(path, "w") as f:
            f.write(str(batch_id))
        
        return batch_id
    
    @staticmethod
    def get_current_id():
        ''' Returns the current batch_id '''
        logger = get_logger(__name__)
        path = AppConfig.BATCH_ID_FILE_PATH
        try:
            with open(path, 'r') as f:
                return int(f.read().strip())
        except ValueError:
            logger.error("❌ Invalid value found in batch_id.txt. Please fix manually.")
            raise ValueError("Invalid batch_id.txt value — expected integer.")
        
    def add_track(self, iTunes_id, track_data):
        self.tracks[iTunes_id] = track_data

    def __len__(self):
        return len(self.tracks)

    def __iter__(self):
        return iter(self.tracks.items())
