# from ScriptingBridge import SBApplication
from src.config.config import AppConfig
from src.logic.playlist_handler import PlaylistHandler
import datetime
import time
import Foundation

class PlaylistManager(): 
    def __init__(self, music_app, logger):
        self.music_app = music_app
        self.user_playlists = {p.name():p for p in self.music_app.userPlaylists()}
        self.logger = logger

    def get_playlist(self, name):
        playlist = self.user_playlists.get(name)
        return PlaylistHandler(self.music_app, playlist) if playlist else None

    def create_playlist(self, name):
        ''' 
        Creates a playlist.
        
        Args:
            name (str): name of the playlist to create
        '''
        new_playlist = self.music_app.classForScriptingClass_("playlist").alloc().initWithProperties_({"name": name})
        self.music_app.sources()[0].playlists().insertObject_atIndex_(new_playlist, 0)
        self.user_playlists = {p.name():p for p in self.music_app.userPlaylists()}
        self.logger.info(f"Created playlist : '{name}'")
    
    def update_genre_playlist(self, mode='Full', target_playlist_names=None):
        '''
        Update genre playlist. 

        Args:
            - mode (str) : 'Full' (All library's tracks) or 'NTO' (New Tracks Only)
            - target_playlist_names (list[str]) : name of the playlists to update. If None, all user's playlists.
        '''
        # === Get tracks to file ==== #
        if mode == 'Full':
            track_set = self.music_app.tracks()
        elif mode == 'NTO':
            track_set = self._get_last_added_track_batch()
        else:
            self.logger.error(f"Unknown mode : {mode}")
        
        # === Get target playlists === #
        if not target_playlist_names:
            target_playlist_names = [pl.name() for pl in self.music_app.userPlaylists()]  # Liste des noms de toutes les playlists de la bibliothèque
        self.logger.info(f"Target playlists : {target_playlist_names}")

        # === Existing playlists cleaning (if Full) === #
        if mode == 'Full':
            for name in target_playlist_names:
                handler = self.get_playlist(name)
                if handler:
                    handler.remove_all_tracks()
                    self.logger.info(f"🗑 Track removing in '{name}'")

        # === Track ordering === #
        for track in track_set:
            track_name = track.name()
            genre = track.genre() 
            track_playlists = [pl.name() for pl in track.playlists()] 
            # Track without genre -> skip
            if not genre:
                self.logger.debug(f"⏭ '{track_name}' ignored : no genre")
                continue  
            # Non-target gender -> skip
            if genre not in target_playlist_names:
                self.logger.debug(f"⏭ '{track_name}' ignored :  '{genre}' is not a target gender")
                continue
            # Track already in genre playlist -> skip
            if genre in track_playlists:
                self.logger.debug(f"⏭ '{track_name}' already in playlist '{genre}'")
                continue
            # Track add to the playlist
            handler = self.get_playlist(genre)
            if not handler:
                self.logger.warning(self.logger.warning(f"❌ Playlist '{genre}' not founded — incorrect or non-existent spelling. Track '{track_name}' ignored."))
                continue
            try:
                handler.add_track(track)
                self.logger.info(f"Track '{track_name}' added to '{genre}'")
            except Exception as e:
                self.logger.error(f"Error add track '{track_name}' → '{genre}': {e}")

    def _get_last_added_track_batch(self):
        ''' Returns the list of the tracks added in the last batch '''
        last_added_track_list = []
        with open(AppConfig.BATCH_ID_FILE_PATH, "r") as f:
            batch_id = f.read().strip()
        for track in self.music_app.tracks():
            if track.comment().endswith(batch_id):
                last_added_track_list.append(track)
        return last_added_track_list

    # def populate_playlist(self, name):
    #     """ Ajoute les musiques à la playlist suivant les règles établies """
    #     playlist = self.get_playlist(name)
    #     hard_music_genres = ["Hardstyle", "Frenchcore", "Raw"]
    #     valid_playlists = ["Musik' 2K23", "Musik' 2K24"]
    #     year = datetime.timedelta(days=365)
    #     now = datetime.datetime.now()

    #     for track in self.music_app.tracks():
    #         #print(track.name())
    #         # Conditions de sélection des tracks
    #         # Musique de moins d'un an & ayant un des genres valides
    #         if track.genre() in hard_music_genres and any(p.name() in valid_playlists for p in track.playlists()):
    #             playlist.add_track(track)

if __name__ == "__main__":
    manager = PlaylistManager('Euphoric Hardstyle')
    print(manager.playlist)
    # manager.populate_playlist()
    # manager.update_genre_playlist("Full", ["Euphoric Hardstyle", "Hardstyle"])
    # manager.remove_all_tracks_from_playlist('Test')
