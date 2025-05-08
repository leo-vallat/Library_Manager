from src.config.logger_config import get_logger
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from itertools import chain
from src.config.config import AppConfig
import json
import os
import random


class SmartPlaylistManager:
    def __init__(self, music_app, playlist_handler, playlist_name, target_size, target_genre=[], include_recent=True, recent_days=30):
        self.music_app = music_app
        self.playlist_handler = playlist_handler  # Instance to manipulate the playlist
        self.playlist_name = playlist_name
        self.target_size = target_size
        self.target_genre = target_genre
        self.include_recent = include_recent
        self.recent_days = recent_days
        self.logger = get_logger(self.__class__.__name__)

        self.history = []  # Track IDs already added before
        self.recent_tracks = []  # Newest tracks to prioritize
        self.track_pool = []  # All eligible tracks

        self._load_history()
        self._load_track_pools()

        self.logger.info('🟢 SmartPlaylistManager initialized')

    def update_playlist(self):
        ''''''
        self.playlist_handler.remove_all_tracks()
        self.logger.debug(f"🗑 Tracks removed in '{self.playlist_name}'")

        selected_tracks = self.recent_tracks

        remaining = self.target_size - len(selected_tracks)
        if remaining > 0:
            selected_tracks += random.sample(self.track_pool, min(remaining, len(self.track_pool)))
        else:
            self.logger.debug("No place remaining after adding recent tracks")

        for track in selected_tracks:
            self.playlist_handler.add_track(track)
            self.logger.info(f"Add to smart playlist '{track.name()} → {self.playlist_name}'")

        timestamp = int(datetime.now().timestamp())
        self.history[timestamp] = [track.persistentID() for track in selected_tracks]

        self._save_history()

        if len(selected_tracks) < self.target_size:
            self.logger.warning(f"❗️ Not enough tracks available to reach {self.target_size} tracks - Please restore history or add new tracks")
        elif len(selected_tracks) > self.target_size:
            self.logger.info(f"More recent tracks added ({len(selected_tracks)}) than choosed target size ({self.target_size})")

    def _load_history(self):
        ''''''
        smart_playlists_folder_path = AppConfig.SMART_PLAYLISTS_FOLDER
        history_path = os.path.join(smart_playlists_folder_path, self.playlist_name,'history.json')
        limit_date = datetime.now() - relativedelta(months=6)
        with open(history_path) as f:
            history = json.load(f)
        
        self.history = {
            k : v 
            for k, v in history.items() 
            if datetime.fromtimestamp(int(k)) > limit_date
        }

    def _load_track_pools(self):
        ''''''
        tracks = self.music_app.tracks()
        history_tracks_id = list(chain.from_iterable(self.history.values()))
        recent_date = datetime.now() - timedelta(days=self.recent_days)
        self._filter_tracks(tracks, history_tracks_id, recent_date)

    def _filter_tracks(self, tracks, history_tracks_id, recent_date):
        ''''''
        for track in tracks:
            # === History Check === #
            if track.persistentID() in history_tracks_id:
                continue
            # === Genre Selection === #
            if track.genre() not in self.target_genre:
                continue
            # === Recent Track Check === #
            if self.include_recent: 
                if datetime.strptime(str(track.dateAdded())[:-6], "%Y-%m-%d %H:%M:%S") > recent_date:
                    self.recent_tracks.append(track)
                    continue
            self.track_pool.append(track)

            if self.include_recent and not self.recent_tracks:
                self.logger.info("Not any recent track detected")

    def _save_history(self):
        ''''''
        smart_playlists_folder_path = AppConfig.SMART_PLAYLISTS_FOLDER
        history_path = os.path.join(smart_playlists_folder_path, self.playlist_name, 'history.json')
        with open(history_path, 'w') as f:
            json.dump(self.history, f, indent=2)
        self.logger.debug("history.json updated")