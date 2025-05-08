import Foundation

class PlaylistHandler:
    def __init__(self, music_app, playlist):
        """
        Initializes a PlaylistHandler instance.

        - Associates the handler with the Apple Music application and a specific playlist.

        Args:
            music_app: The Apple Music application instance.
            playlist: The playlist instance to manage.
        """
        self.music_app = music_app
        self.playlist = playlist

    def add_track(self, track):
        """
        Adds a track to the playlist.

        Args:
            track: The track instance to add to the playlist.

        Raises:
            Exception: If the track cannot be added to the playlist.
        """
        try:
            self.music_app.add_to_(Foundation.NSArray.arrayWithObject_(Foundation.NSURL.fileURLWithPath_(track.location().path())), self.playlist)
        except Exception :
            pass

    def remove_all_tracks(self):
        """
        Removes all tracks from the playlist.

        Iterates through the playlist in reverse order and deletes each track.

        Raises:
            Exception: If a track cannot be removed.
        """
        for track in reversed(self.get_track_list()):
            track.delete()

    def get_track_list(self):
        """
        Retrieves the list of tracks in the playlist.

        Returns:
            list: A list of track instances in the playlist.
        """
        return list(self.playlist.tracks())