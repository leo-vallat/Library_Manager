from src.config.config import AppConfig
import json
import os


def create_smart_playlist_files(playlist_name):
        """
        Creates the smart playlist folder and files
        - history.json : all the previous tracks of the playlist
        - tracks.json : the actual tracks of the playlist
        """
        smart_playlists_folder_path = AppConfig.SMART_PLAYLISTS_FOLDER
        playlist_folder_path = os.path.join(smart_playlists_folder_path, playlist_name)
        history_path = os.path.join(playlist_folder_path, 'history.json')
        
        os.mkdir(playlist_folder_path)
        with open(history_path, 'w') as f:
            json.dump({}, f)

def smart_playlist_files_exists(playlist_name):
        """
        
        """
        smart_playlists_folder_path = AppConfig.SMART_PLAYLISTS_FOLDER
        playlist_folder_path = os.path.join(smart_playlists_folder_path, playlist_name)
        history_path = os.path.join(playlist_folder_path, 'history.json')

        return os.path.exists(playlist_folder_path) and os.path.exists(history_path)


if __name__ == '__main__':
    create_smart_playlist_files('test')