import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv


class SpotifyDataGetter:
    def __init__(self):
        load_dotenv('.env')
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        self.spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)



    def get_track_data(self, track_name, artist_name):
        # Rechercher le morceau par titre et artiste
        result = self.spotify.search(q=f'track:{track_name.strip()} artist:{artist_name.strip()}', type='track', limit=1)

        if result['tracks']['items']:
            track_id = result['tracks']['items'][0]['id']
            artwork_url = result['tracks']['items'][0]['album']['images'][0]['url']

            return {
            'spotify_id': track_id,
            'artwork_url': artwork_url
            }

        else:
            return print("Morceau non trouvé.")


###################################################################################################
# Exemple d'utilisation
# spotify = SpotifyDataGetter()

# track_name = "Parachute"
# artist_name = "Wasted Penguinz, Jay Reeve"
# track_data = spotify.get_track_data(track_name, artist_name)

# print(track_data)
###################################################################################################