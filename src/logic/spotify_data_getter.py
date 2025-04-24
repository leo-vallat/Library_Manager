from src.config.logger_config import get_logger
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import spotipy


class SpotifyDataGetter:
    """
    A class to interact with the Spotify API and retrieve track data.

    - Uses Spotipy for Spotify API integration.
    - Loads Spotify credentials from a `.env` file.
    """

    def __init__(self):
        """
        Initializes the SpotifyDataGetter instance.
        """
        load_dotenv('.env')
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        self.spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        self.logger = get_logger(self.__class__.__name__)


    def get_track_data(self, track_name, artist_name):
        """
        Retrieves track data from Spotify based on the track name and artist name.

        - Searches for the track using the Spotify API.
        - Retrieves the Spotify track ID and artwork URL if the track is found.

        Args:
            track_name (str): The name of the track to search for.
            artist_name (str): The name of the artist associated with the track.

        Returns:
            dict: A dictionary containing:
                - 'spotify_id' (str or None): The Spotify ID of the track, or None if not found.
                - 'artwork_url' (str or None): The URL of the track's artwork, or None if not found.
        """
        # Rechercher le morceau par titre et artiste
        result = self.spotify.search(q=f'track:{track_name.strip()} artist:{artist_name.strip()}', type='track', limit=1)

        if result['tracks']['items']:
            self.logger.debug(f"Track data found : '{track_name} - {artist_name}'")
            track_id = result['tracks']['items'][0]['id']
            artwork_url = result['tracks']['items'][0]['album']['images'][0]['url']
        else:
            self.logger.warning(f"❌ Track data of '{track_name} - {artist_name}' not found")
            track_id = None
            artwork_url = None
        
        return {
            'spotify_id': track_id,
            'artwork_url': artwork_url
            }



###################################################################################################
# Exemple d'utilisation
# spotify = SpotifyDataGetter()

# track_name = "Parachute"
# artist_name = "Wasted Penguinz, Jay Reeve"
# track_data = spotify.get_track_data(track_name, artist_name)

# print(track_data)
###################################################################################################