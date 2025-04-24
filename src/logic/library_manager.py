from ScriptingBridge import SBApplication
from src.config.config import AppConfig
from src.config.logger_config import get_logger, log_session_start
from src.logic.playlist_manager import PlaylistManager
from src.logic.track_renamer import TrackRenamer
from src.utils import library_manager_utils
import os
import time


class LibraryManager():
    def __init__(self):
        self.music_app = SBApplication.applicationWithBundleIdentifier_("com.apple.Music")  # Connexion à Musique
        self.logger = get_logger(self.__class__.__name__)
        self.playlists = PlaylistManager(self.music_app)
        self.batch_id = None
        self.added_db = {}
        log_session_start(self.logger)
        AppConfig.validate()
        self.logger.info('LibraryManager initialized')

    def add_tracks(self):
        '''
        Déplace les musiques du dossier de téléchargement vers le dossier d'ajout à Musique. 
        '''
        self.logger.info("Adding tracks to the library")
        self.batch_id = library_manager_utils.get_batch_id()
        for filename in os.listdir(AppConfig.DOWNLOADED_MUSIC_FOLDER_PATH):
            if filename.endswith(AppConfig.AVAILABLE_FILE_EXTENSION):
                self.logger.debug(f"Adding {filename}")
                track_path = os.path.join(AppConfig.DOWNLOADED_MUSIC_FOLDER_PATH, filename)
                result = library_manager_utils.add_track(track_path)
                if result.returncode != 0:
                    self.logger.error(f"❌ Error while adding track '{filename}' → {result.stderr.strip()}")

                time.sleep(1)  # Wait for the track to be added

                iTunes_track_ID = self._get_last_added_track().persistentID()
                self.added_db[iTunes_track_ID] = library_manager_utils.format_track_data(filename)
                self.logger.info(f"✅ {self.added_db[iTunes_track_ID]['title']} - {self.added_db[iTunes_track_ID]['artist']} added")


    def rename_tracks(self): 
        ''' Rename tracks in self.added_db '''
        renamer = TrackRenamer()

        for iTunes_track_ID in self.added_db:
            track_data = self.added_db[iTunes_track_ID]

            release_year = track_data['release_year']
            title = track_data['title']
            artist = track_data['artist']
            album = track_data['album']
            IDs = str(iTunes_track_ID) + ' | ' + track_data['spotify_id'] + ' | ' + str(self.batch_id)
            artwork_path = track_data['artwork_path']
             
            renamer.set_values(iTunes_track_ID, title, artist, album, release_year, IDs, artwork_path)
            renamer.rename_track()
            self._remove_artwork(iTunes_track_ID)
            self.logger.info(f"✅ {title} - {artist} renamed")

    def _get_last_added_track(self):
        '''
        Retourne la dernière musique ajoutée à la bibliothèque

        Return : 
            - track : La dernière musique ajoutée
        '''
        tracks = self.music_app.tracks()
        return sorted(tracks, key=lambda track: track.dateAdded(), reverse=True)[0]

    def _remove_artwork(self, iTunes_track_ID):
        ''' Remove artwork '''
        artwork_path = self.added_db[iTunes_track_ID]['artwork_path']
        if artwork_path:
            if os.path.exists(artwork_path):
                os.remove(self.added_db[iTunes_track_ID]['artwork_path'])
                self.logger.debug(f"Artwork removed")
            else:
                self.logger.warning(f"❌ Artwork path {artwork_path} doesn't exists")