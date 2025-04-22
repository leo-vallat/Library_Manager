from ScriptingBridge import SBApplication
from src.config.config import AppConfig
from src.config.logger_config import get_logger, log_session_start
from src.logic.TrackRenamer import TrackRenamer
from src.logic.SpotifyDataGetter import SpotifyDataGetter
from src.utils import library_manager_utils
import os
import requests
import subprocess
import time


class LibraryManager():
    def __init__(self):
        self.music_app = SBApplication.applicationWithBundleIdentifier_("com.apple.Music")  # Connexion à Musique
        self.downloaded_music_path = AppConfig.DOWNLOADED_MUSIC_FOLDER_PATH  # Chemin vers le dossier de téléchargement
        self.batch_id = None
        self.added_db = {}
        self.logger = get_logger(self.__class__.__name__)
        log_session_start(self.logger)
        AppConfig.validate()
        self.logger.info('LibraryManager initialized')

    def add_tracks(self):
        '''
        Déplace les musiques du dossier de téléchargement vers le dossier d'ajout à Musique. 
        '''
        spotify = SpotifyDataGetter()
        self.batch_id = library_manager_utils.get_batch_id()
        for filename in os.listdir(self.downloaded_music_path):
            if filename.endswith(AppConfig.AVAILABLE_FILE_EXTENSION):
                music_path = os.path.join(self.downloaded_music_path, filename)

                subprocess.run(['open', '-a', 'Music', music_path])  # Ajout de la track à la bibliothèque

                time.sleep(1)  # Attente que la track soit ajoutée à la bibliothèque

                track = self._get_last_added_track()  # Récupération de la track ajoutée
                iTunes_track_ID = track.persistentID()  # ID attribuée à la track dans Musique

                if filename.endswith('.aiff'):
                    track_parts = filename[:-5].split('%')  # Séparation du nom de la track
                else:
                    track_parts = filename[:-4].split('%')  # Séparation du nom de la track

                #  Vérification qu'il y ait bien 4 parties différentes (sinon la partie est créée et vaut '')
                while len(track_parts) < 4 :
                    track_parts.append('')
                
                track_data = {'release_year' : track_parts[0], 'title' : track_parts[1], 'artist' : track_parts[2], 'album' : track_parts[3]}

                #  Ajout de l'id spotify et de l'url de l'artwork 
                track_data.update(spotify.get_track_data(track_parts[1], track_parts[2]))

                # Nettoyage des track_datas
                track_data['title'], track_data['artist'], track_data['album'] = library_manager_utils.clean_track_elements(track_data['title'], track_data['artist'], track_data['album'])
                
                # Artwork
                if filename.endswith(('.aiff', '.m4a')):
                    track_data['artwork_path'] = None
                else:
                    track_data['artwork_path'] = os.path.abspath(self._dl_artwork(track_data['title'], track_data['artist'], track_data['artwork_url']))
                del track_data['artwork_url']

                self.added_db[iTunes_track_ID] = track_data  # Ajout de l'ID et des informations de la track au dictionnaire

                self.logger.info(f"Track : {track_data['title']} - {track_data['artist']} added")

    def rename_tracks(self): 
        '''
        Itère sur les éléments du dictionnaire et renomme les photos
        '''
        renamer = TrackRenamer()

        for iTunes_track_ID in self.added_db:  # Itération sur les éléments du dictionnaire
            track_data = self.added_db[iTunes_track_ID]

            release_year = track_data['release_year']  # Année de sortie
            title = track_data['title']  # Titre
            artist = track_data['artist']  # Artiste
            album = track_data['album']  # Album
            IDs = str(iTunes_track_ID) + ' | ' + track_data['spotify_id'] + ' | ' + str(self.batch_id)  # ID iTunes & Spotify
            artwork_path = track_data['artwork_path']  # Artwork Path
            
            renamer.set_values(iTunes_track_ID, title, artist, album, release_year, IDs, artwork_path)  # Fixe les valeurs des attributs du TrackRenamer
            renamer.rename_track()  # Renommage de la track

            self._remove_artwork(iTunes_track_ID)# Suppression de l'artwork 

    def _get_last_added_track(self):
        '''
        Retourne la dernière musique ajoutée à la bibliothèque

        Return : 
            - track : La dernière musique ajoutée
        '''
        tracks = self.music_app.tracks()
        track = sorted(tracks, key=lambda track: track.dateAdded(), reverse=True)[0]
        return track

    def _dl_artwork(self, title, artist, artwork_url):
        ''' Télécharge l'artwork '''
        artwork_path = f'ressources/artwork/{title}-{artist}.jpg'
        # Téléchargement et enregistrement de l'artwork
        response = requests.get(artwork_url)
        if response.status_code == 200:  # Check if the request was successful
            with open(artwork_path, "wb") as file:
                file.write(response.content)
        else:
            self.logger.error(f"Failed to download image. Status code: {response.status_code}")
        return artwork_path  

    def _remove_artwork(self, iTunes_track_ID):
        ''' Remove artwork '''
        artwork_path = self.added_db[iTunes_track_ID]['artwork_path']
        if artwork_path and os.path.exists(artwork_path):
            os.remove(self.added_db[iTunes_track_ID]['artwork_path'])
        else:
            self.logger.error(f"Failed to remove artwork : {artwork_path}")