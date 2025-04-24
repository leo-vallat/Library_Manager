from src.config.config import AppConfig
from src.config.logger_config import get_logger

class Batch:    
    def __init__(self, batch_id : int):
        """
        Initializes a Batch instance.

        - Sets the batch ID.
        - Initializes an empty dictionary to store tracks.
        - Sets up the logger for the class.

        Args:
            batch_id (int): The unique identifier for the batch.
        """
        self.logger = get_logger(self.__class__.__name__)
        self.id = batch_id
        self.tracks = {} 
        self.logger.debug(f"New batch started (ID={self.id})")

    @classmethod
    def new(cls):
        """
        Creates a new batch with an auto-incremented ID.

        Returns:
            Batch: A new Batch instance.
        """
        batch_id = cls.get_new_id()
        return cls(batch_id)
    
    @classmethod
    def from_current_id(cls):
        """
        Loads the last added batch using the current batch ID.

        Returns:
            Batch: A Batch instance for the current batch ID.
        """
        batch_id = cls.get_current_id()
        return cls(batch_id)
    
    @classmethod
    def from_existing_id(cls, batch_id : int):
        """
        Loads an existing batch using a specific batch ID.

        Args:
            batch_id (int): The ID of the batch to load.

        Returns:
            Batch: A Batch instance for the specified batch ID.
        """
        return cls(batch_id)

    @staticmethod
    def get_new_id():
        """
        Generates a new batch ID by incrementing the current batch ID.

        - Reads the current batch ID from a file.
        - Increments the ID and writes it back to the file.

        Returns:
            int: The new batch ID.

        Raises:
            ValueError: If the batch ID file contains an invalid value.
        """
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
        """
        Retrieves the current batch ID from the batch ID file.

        Returns:
            int: The current batch ID.

        Raises:
            ValueError: If the batch ID file contains an invalid value.
        """
        logger = get_logger(__name__)
        path = AppConfig.BATCH_ID_FILE_PATH
        try:
            with open(path, 'r') as f:
                return int(f.read().strip())
        except ValueError:
            logger.error("❌ Invalid value found in batch_id.txt. Please fix manually.")
            raise ValueError("Invalid batch_id.txt value — expected integer.")
        
    def add_track(self, iTunes_id, track_data):
        """
        Adds a track to the batch.

        Args:
            iTunes_id: The unique identifier for the track in iTunes.
            track_data (dict): Metadata for the track.
        """
        self.tracks[iTunes_id] = track_data

    def __len__(self):
        """
        Returns the number of tracks in the batch.

        Returns:
            int: The number of tracks in the batch.
        """
        return len(self.tracks)

    def __iter__(self):
        """
        Returns an iterator over the tracks in the batch.

        Yields:
            tuple: A tuple containing the iTunes ID and track data for each track.
        """
        return iter(self.tracks.items())
