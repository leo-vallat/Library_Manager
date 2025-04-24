from ScriptingBridge import SBApplication
from src.config.config import AppConfig
from src.config.logger_config import get_logger, log_session_start
from src.logic.batch import Batch
from src.logic.track_renamer import TrackRenamer
from src.playlist_manager import PlaylistManager
from src.utils import library_manager_utils
import os
import time


class LibraryManager():
    def __init__(self):
        """
        Initializes the LibraryManager instance.

        - Connects to the Apple Music application using ScriptingBridge.
        - Sets up the logger for the class.
        - Validates the application configuration.
        - Initializes the playlist manager.

        Raises:
            Exception: If the connection to Apple Music or configuration validation fails.
        """
        self.music_app = SBApplication.applicationWithBundleIdentifier_("com.apple.Music")
        self.logger = get_logger(self.__class__.__name__)
        log_session_start(self.logger)
        AppConfig.validate()
        self.logger.info('🟢 LibraryManager initialized')
        self.playlists = PlaylistManager(self.music_app)

    def add_tracks(self, rename=True):
        """
        Adds music files from the download folder to the Apple Music library.

        - Iterates through files in the download folder.
        - Adds compatible files to the library.
        - Optionally renames the added tracks.

        Args:
            rename (bool): Whether to rename tracks after adding them. Defaults to True.

        Raises:
            Exception: If an error occurs while adding a track.
        """
        self.logger.info("▶️ Adding tracks to the library")
        self.batch = Batch.new()

        for filename in os.listdir(AppConfig.DOWNLOADED_MUSIC_FOLDER_PATH):
            if filename.endswith(AppConfig.AVAILABLE_FILE_EXTENSION):
                self.logger.debug(f"Adding {filename}")
                track_path = os.path.join(AppConfig.DOWNLOADED_MUSIC_FOLDER_PATH, filename)
                
                result = library_manager_utils.add_track(track_path)
                if result.returncode != 0:
                    self.logger.error(f"❌ Error while adding track '{filename}' → {result.stderr.strip()}")

                time.sleep(1)  # Wait for the track to be added

                iTunes_track_ID = self._get_last_added_track().persistentID()
                track_data = library_manager_utils.format_track_data(filename)
                self.batch.add_track(iTunes_track_ID, track_data)
                self.logger.info(f"Add {track_data['title']} - {track_data['artist']}")

        if rename and len(self.batch):
            if len(self.batch) == 1:
                time.sleep(1)
            self._rename_batch()

    def _rename_batch(self): 
        """
        Renames tracks in the current batch.

        - Updates metadata for each track in the batch.
        - Removes associated artwork after renaming.

        Raises:
            Exception: If an error occurs during renaming.
        """
        renamer = TrackRenamer()

        for iTunes_track_ID, track_data in self.batch:
            title = track_data['title']
            artist = track_data['artist']
            album = track_data['album']
            release_year = track_data['release_year']
            IDs = str(iTunes_track_ID) + ' | ' + track_data['spotify_id'] + ' | ' + str(self.batch.id)
            artwork_path = track_data['artwork_path']
             
            renamer.set_values(iTunes_track_ID, title, artist, album, release_year, IDs, artwork_path)
            renamer.rename_track()
            self._remove_artwork(iTunes_track_ID)
            self.logger.info(f"Renamed {title} - {artist}")

    def _get_last_added_track(self):
        """
        Retrieves the most recently added track in the Apple Music library.

        Returns:
            track: The most recently added track.
        """
        tracks = self.music_app.tracks()
        return sorted(tracks, key=lambda track: track.dateAdded(), reverse=True)[0]

    def _remove_artwork(self, iTunes_track_ID):
        """
        Removes the artwork associated with a track.

        - Deletes the artwork file from the filesystem if it exists.

        Args:
            iTunes_track_ID (str): The ID of the track whose artwork should be removed.

        Logs:
            - Debug: If the artwork is successfully removed.
            - Warning: If the artwork file does not exist.
        """
        artwork_path = self.batch.tracks[iTunes_track_ID]['artwork_path']
        if artwork_path:
            if os.path.exists(artwork_path):
                os.remove(self.batch.tracks[iTunes_track_ID]['artwork_path'])
                self.logger.debug(f"Artwork removed")
            else:
                self.logger.warning(f"❌ Artwork path {artwork_path} doesn't exists")