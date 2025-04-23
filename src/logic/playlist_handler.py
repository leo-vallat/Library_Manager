import Foundation

class PlaylistHandler:
    def __init__(self, music_app, playlist):
        self.music_app = music_app
        self.playlist = playlist

    def add_track(self, track):
        ''' Add the track to self.playlist '''
        self.music_app.add_to_(Foundation.NSArray.arrayWithObject_(Foundation.NSURL.fileURLWithPath_(track.location().path())), self.playlist)

    def remove_all_tracks(self):
        '''
        Remove all the track from a specific playlist

        Args:
            playlist (str): the name of the playlist
        '''
        for track in reversed(self.get_track_list()):
            track.delete()

    def get_track_list(self):
        ''' 
        Returns the list of the track instances in a playlist 
        '''
        return list(self.playlist.tracks())