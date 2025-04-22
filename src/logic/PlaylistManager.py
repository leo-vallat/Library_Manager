import datetime
import time
from ScriptingBridge import SBApplication
import Foundation

class PlaylistManager(): 
    def __init__(self, name=None, size=None):
        """
        Constructeur du gestionnaire de playlist

        Args:
            name : le nom de la playlist
            size : la taille de la playlist en nombre de track
        """
        self.name = name
        self.size = size
        self.music_app = SBApplication.applicationWithBundleIdentifier_("com.apple.Music")
        self.playlist = self.initialize_playlist(name)

    def initialize_playlist(self, name):
        '''
        Test l'existence de la playlist, si False la crée
        '''
        if self.name == None:
            return None
        elif self.playlist_is_existing():
            return self.get_app_playlist()
        return self.create_playlist()

    def playlist_is_existing(self):
        """
        Recherche la playlist ayant pour nom self.name dans les playlist existante de Musique

        Return:
            True : Si la playlist existe
            False : Si la playlist n'existe
        """
        for playlist in self.music_app.userPlaylists():
            if self.name == playlist.name():
                return True
        return False

    def get_app_playlist(self):
        for playlist in self.music_app.userPlaylists():
            if self.name == playlist.name():
                return playlist

    def create_playlist(self):
        """
        Méthode de création d'une playlist
        """
        new_playlist = self.music_app.classForScriptingClass_("playlist").alloc().initWithProperties_({"name": self.name})
        self.music_app.sources()[0].playlists().insertObject_atIndex_(new_playlist, 0)
        print(f"La playlist '{self.name}' a été créée.")
    
    def populate_playlist(self):
        """ Ajoute les musiques à la playlist suivant les règles établies """
        hard_music_genres = ["Hardstyle", "Frenchcore", "Raw"]
        valid_playlists = ["Musik' 2K23", "Musik' 2K24"]
        year = datetime.timedelta(days=365)
        now = datetime.datetime.now()

        for track in self.music_app.tracks():
            #print(track.name())
            # Conditions de sélection des tracks
            # Musique de moins d'un an & ayant un des genres valides
            if track.genre() in hard_music_genres and any(p.name() in valid_playlists for p in track.playlists()):
                self.add_track(track)

    def add_track(self, track):
        ''' Ajoute une track à une playlist '''
        try:
            print(f'{track.name()} added')
            self.music_app.add_to_(Foundation.NSArray.arrayWithObject_(Foundation.NSURL.fileURLWithPath_(track.location().path())), self.playlist)
        except Exception as e:
            print(f"Erreur lors de l'ajout de la track {track} à la playlist {self.playlist} : \n {e}")

    def update_genre_playlist(self, set, target_playlist_list=[]):
        '''
        Met à jour les playlists de genre

        Args:
            - set : 'Full' -> mise à jour sur toutes les musiques de la bibliothèque / 'NTO' (New Tracks Only) -> mise à jour seulement sur les dernières tracks téléchargées
            - target_playlist_list : liste des noms des playlists qui doivent être mise à jour
        '''
        if set == 'Full':
            track_set = self.music_app.tracks()
            for playlist in target_playlist_list:
                print(playlist)
                self.remove_all_tracks_from_playlist(playlist)
        elif set == 'NTO':
            track_set = self.get_last_added_track_list()

        # Si aucune liste de playlist n'est fournie en paramètre
        if len(target_playlist_list) == 0:
            target_playlist_list = [pl.name() for pl in self.music_app.userPlaylists()]  # Liste des noms de toutes les playlists de la bibliothèque

        for track in track_set:
            genre = track.genre()  # Récupère le genre de la track

            track_playlists = [pl.name() for pl in track.playlists()]  # Liste des noms des playlists dans lesquelles se trouve la track
            
            # Si la track n'a pas de genre, passe à la suivante
            if not genre:
                print(track.name(), ' : ', genre)
                print('not to add : No genre', '\n')
                continue  
            # Si la track est déjà dans la playlist de genre, passe à la suivante
            if genre in track_playlists:
                print(track.name(), ' : ', genre)
                print("not to add : track's genre already in the playlist set")
                continue
            # Si le genre ne fait pas parti de la liste des playlist ciblée par la mise à jour, passe à la suivante
            if genre not in target_playlist_list:
                print(track.name(), ' : ', genre)
                print("not to add : track's genre not to be classfied")
                continue
            
            self.set_name(genre)
            self.set_playlist()  
            self.add_track(track)

    def get_last_added_track_list(self):
        ''' Return the list of the track added the last time '''
        last_added_track_list = []
        batch_id_path = 'ressources/batch_id.txt'

        with open(batch_id_path, "r") as f:
            batch_id = f.read().strip()
        for track in self.music_app.tracks():
            if track.comment().endswith(batch_id):
                last_added_track_list.append(track)
        
        return last_added_track_list

    def remove_all_tracks_from_playlist(self, playlist):
        '''
        Remove all the track from a specific playlist

        Args:
            playlist (str): the name of the playlist
        '''
        tracks = self.get_tracks_from_playlist(playlist)
        self.set_name(playlist)
        self.set_playlist()
        for track in reversed(tracks):
            self.remove_track(track)

    def get_tracks_from_playlist(self, playlist_name):
        ''' 
        Returns the list of the track instances in a playlist 
        '''
        try:
            for playlist in self.music_app.userPlaylists():
                if playlist.name() == playlist_name:
                    return list(playlist.tracks())
            print(f"Aucune playlist nommée '{playlist_name}' n'a été trouvée.")
            return []
        except Exception as e:
            print(f"Erreur lors de la récupération des tracks de la playlist '{playlist_name}' : \n {e}")
            return []
    
    def remove_track_from_playlist(self, track, playlist):
            '''
            Removes a specific track from a specific playlist.

            Args:
                - track: The track object to remove.
                - playlist: The playlist object from which to remove the track.
            '''
            try:
                # Check if the track is in the playlist
                if track in playlist.tracks():
                    self.remove_track(track)
                else:
                    print(f"Track '{track.name()}' is not in playlist '{playlist.name()}'.")
            except Exception as e:
                print(f"Error removing track '{track.name()}' from playlist '{playlist.name()}': {e}")

    def remove_track(self, track):
        ''' Remove the track from self.playlist '''
        try:
            track.delete()
            print(f'{track.name()} removed')
        except Exception as e:
            print(f"Erreur lors de la suppression de la track {track} de la playlist {self.playlist} : \n {e}")

if __name__ == "__main__":
    manager = PlaylistManager('Euphoric Hardstyle')
    print(manager.playlist)
    # manager.populate_playlist()
    # manager.update_genre_playlist("Full", ["Euphoric Hardstyle", "Hardstyle"])
    # manager.remove_all_tracks_from_playlist('Test')
