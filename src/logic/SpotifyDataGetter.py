import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv


class SpotifyDataGetter:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        self.spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)



    def get_track_data(self, track_name, artist_name):
        # Rechercher le morceau par titre et artiste
        result = self.spotify.search(q=f'track:{track_name.strip()} artist:{artist_name.strip()}', type='track', limit=1)
        
        print(result['tracks']['items'][0]['id'])
        print('\n')

        if result['tracks']['items']:
            track_id = result['tracks']['items'][0]['id']
            
            # Obtenir les "audio features" du morceau
            track_features = self.spotify.audio_features([track_id])[0]
            
            # Récupérer le BPM, l'énergie et la clé du morceau
            bpm = track_features['tempo']
            energy = track_features['energy']
            key = track_features['key']
            mode = track_features['mode']
            happiness = track_features['valence']
            danceability = track_features['danceability']
            loudness = track_features['loudness']
            speechiness = track_features['speechiness']
            spotify_id = track_features['id']
            
            # Conversion de la clé Spotify en clé Camelot
            camelot_key = self.get_camelot_key(key, mode)
            
            return {
                'BPM': round(bpm),
                'key': camelot_key,
                'energy': self.discretize_value(energy),
                'happiness': round(happiness*100),
                'danceability': round(danceability*100),
                'loudness': str(round(loudness)) +' dB',
                'speechiness':str(round(speechiness*100)),
                'spotify_id': str(spotify_id)
            }
        else:
            return print("Morceau non trouvé.")



    def get_camelot_key(self, key, mode):
        camelot_wheel_major = {
            0: '8B', 1: '3B', 2: '10B', 3: '5B', 4: '12B', 5: '7A', 6: '2B',
            7: '9B', 8: '4B', 9: '11B', 10: '6B', 11: '1B'
        }
        camelot_wheel_minor = {
            0: '5A', 1: '12A', 2: '7A', 3: '2A', 4: '9A', 5: '4A', 6: '11A',
            7: '6A', 8: '1A', 9: '8A', 10: '3A', 11: '10A'
        }
        return camelot_wheel_major[key] if mode == 1 else camelot_wheel_minor[key]

 
    def discretize_value(self, value: float) -> int:
        '''
        Discrétise la valeur de l'énergie suivant les valeurs admissibles
        '''
        value *= 100 
        admissible_values = [0, 20, 40, 60, 80, 100]  # Liste des valeurs admissibles
        closest_value = min(admissible_values, key=lambda x: abs(x - value))  # Trouve la valeur admissible la plus proche

        return closest_value
    


###################################################################################################
# Exemple d'utilisation
spotify = SpotifyDataGetter()

track_name = "Parachute"
artist_name = "Wasted Penguinz, Jay Reeve"
track_data = spotify.get_track_data(track_name, artist_name)

print(track_data)
###################################################################################################