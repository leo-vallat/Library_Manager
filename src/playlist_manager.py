from src.config.config import AppConfig
from src.config.logger_config import get_logger
from src.logic.batch import Batch
from src.logic.playlist_handler import PlaylistHandler
from src.logic.smart_playlist_manager import SmartPlaylistManager
from src.utils.playlist_manager_utils import create_smart_playlist_files, smart_playlist_files_exists

class PlaylistManager(): 
    def __init__(self, music_app):
        """
        Removes the artwork associated with a track.

        - Deletes the artwork file from the filesystem if it exists.

        Args:
            iTunes_track_ID (str): The ID of the track whose artwork should be removed.
        """
        self.music_app = music_app
        self.user_playlists = {p.name():p for p in self.music_app.userPlaylists()}
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('🟢 PlaylistManager initialized')

    def get_playlist(self, name):
        """
        Retrieves a playlist by its name.

        Args:
            name (str): The name of the playlist to retrieve.

        Returns:
            PlaylistHandler: A handler for the playlist if found, otherwise None.
        """
        playlist = self.user_playlists.get(name)
        return PlaylistHandler(self.music_app, playlist) if playlist else None

    def create_playlist(self, name):
        ''' 
        Creates a new playlist.
        
        Args:
            name (str): The name of the playlist to create.
        '''
        new_playlist = self.music_app.classForScriptingClass_("playlist").alloc().initWithProperties_({"name": name})
        self.music_app.sources()[0].playlists().insertObject_atIndex_(new_playlist, 0)
        self.user_playlists = {p.name():p for p in self.music_app.userPlaylists()}
        self.logger.info(f"▶️ Created playlist : '{name}'")
    
    def update_genre_playlist(self, mode='NTO', target_playlist_names=None):
        '''
        Update genre playlists based on the specific mode. 

        - In 'NTO' mode, only tracks from the last batch are considered.
        - In 'Full' mode, all tracks in the library are considered.
        - Tracks are added to playlists matching their genre.

        Args:
            - mode (str) : 'NTO' (New Tracks Only) or 'Full' (All library's tracks)
            - target_playlist_names (list[str]) : name of the playlists to update. If None, all user's playlists.
        '''
        self.logger.info(f"▶️ Updating genre playlists in {mode} mode")
        # === Get tracks to file ==== #
        if mode == 'NTO':
            track_set = self._get_last_added_track_batch()
        elif mode == 'Full':
            track_set = self.music_app.tracks()
        else:
            self.logger.error(f"❌ Unknown mode : {mode}")
            return
        
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
                    self.logger.debug(f"🗑 Tracks removed in '{name}'")

        # === Track ordering === #
        for track in track_set:
            track_name = track.name()
            genre = track.genre() 
            track_playlists = [pl.name() for pl in track.playlists()] 
            # Track without genre -> skip
            if not genre:
                self.logger.debug(f"⏭ '{track_name}' ignored - no genre")
                continue  
            # Non-target gender -> skip
            if genre not in target_playlist_names:
                self.logger.debug(f"⏭ '{track_name}' ignored - '{genre}' is not a target gender")
                continue
            # Track already in genre playlist -> skip
            if genre in track_playlists:
                self.logger.debug(f"⏭ '{track_name}' already in playlist '{genre}'")
                continue
            # Track add to the playlist
            handler = self.get_playlist(genre)
            if not handler:
                self.logger.warning(f"❌ Playlist '{genre}' not founded — incorrect or non-existent spelling - Track '{track_name}' ignored.")
                continue
            try:
                handler.add_track(track)
                self.logger.info(f"Add to genre playlist '{track_name} → {genre}'")
            except Exception as e:
                self.logger.error(f"❌ Error while adding track '{track_name}' → '{genre}': {e}")

    def _get_last_added_track_batch(self):
        """
        Retrieves the list of tracks added in the last batch.

        Returns:
            list: A list of tracks added in the last batch.
        """
        last_added_track_list = []
        batch_id = Batch.get_current_id()
        for track in self.music_app.tracks():
            if track.comment().endswith(batch_id):
                last_added_track_list.append(track)
        return last_added_track_list

    def manage(self, playlist_name, target_size, target_genre, include_recent=True, recent_days=30):
        ''''''
        if playlist_name not in self.user_playlists:
            self.logger.info(f"▶️ Creating and filling {playlist_name} playlist")
            self.create_playlist(playlist_name)
            create_smart_playlist_files(playlist_name)
            self.logger.debug(f"{playlist_name} management files created")
        else:
            self.logger.info(f"▶️ Updating {playlist_name} playlist")
        playlist_handler = self.get_playlist(playlist_name)
        smart_playlist_manager = SmartPlaylistManager(self.music_app, playlist_handler, playlist_name, target_size, target_genre, include_recent, recent_days)
        smart_playlist_manager.update_playlist()

    def restore_history(self, playlist_name, last_day_to_keep: int=None):
        ''''''
        if playlist_name in self.user_playlists:
            if smart_playlist_files_exists(playlist_name):
                SmartPlaylistManager(playlist_name=playlist_name).restore_history(last_day_to_keep)
            else:
                self.logger.warning(f"❗️ Playlist '{playlist_name}' files doesn't exist")
        else:
            self.logger.warning(f"❗️ Playlist '{playlist_name}' doesn't exists in Apple Music")

if __name__ == "__main__":
    manager = PlaylistManager('Euphoric Hardstyle')
    print(manager.playlist)
    # manager.populate_playlist()
    # manager.update_genre_playlist("Full", ["Euphoric Hardstyle", "Hardstyle"])
    # manager.remove_all_tracks_from_playlist('Test')
