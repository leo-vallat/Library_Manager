from ScriptingBridge import SBApplication
from src.logic.TrackRenamer import TrackRenamer
from src.logic.SpotifyDataGetter import SpotifyDataGetter
from dotenv import load_dotenv
import os
import regex as re
import requests
import subprocess
import time



class LibraryManager(): 
    def __init__(self):
        """
        Constructeur du manager de bibliothèque
        """
        load_dotenv('.env')
        self.music_app = SBApplication.applicationWithBundleIdentifier_("com.apple.Music")  # Connexion à Musique
        self.downloaded_music_path = os.getenv('DOWNLOADED_MUSIC_FOLDER_PATH')  # Chemin vers le dossier de téléchargement
        self.added_db = {}



    def get_last_added_track(self):
        '''
        Retourne la dernière musique ajoutée à la bibliothèque

        Return : 
            - track : La dernière musique ajoutée
        '''
        tracks = self.music_app.tracks()
        track = sorted(tracks, key=lambda track: track.dateAdded(), reverse=True)[0]
        return track



    def add_tracks(self):
        '''
        Déplace les musiques du dossier de téléchargement vers le dossier d'ajout à Musique. 
        '''
        spotify = SpotifyDataGetter()
        for filename in os.listdir(self.downloaded_music_path):
            if filename.endswith(('.mp3', '.wav',  '.aiff', '.m4a')):
                music_path = os.path.join(self.downloaded_music_path, filename)

                subprocess.run(['open', '-a', 'Music', music_path])  # Ajout de la track à la bibliothèque

                time.sleep(1)  # Attente que la track soit ajoutée à la bibliothèque

                track = self.get_last_added_track()  # Récupération de la track ajoutée
                iTunes_track_ID = track.persistentID()  # ID attribuée à la track dans Musique

                if filename.endswith('.aiff'):
                    track_parts = filename[:-5].split('%')  # Séparation du nom de la track
                else:
                    track_parts = filename[:-4].split('%')  # Séparation du nom de la track

                #  Vérification qu'il y ait bien 4 parties différentes (sinon la partie est créée et vaut '')
                while len(track_parts) < 4 :
                    track_parts.append('')
                
                track_data = {'release_year' : track_parts[0], 'title' : track_parts[1], 'artist' : track_parts[2], 'album' : track_parts[3]}

                #  Ajout de l'id spotify et de l'url de l'artwork 
                track_data.update(spotify.get_track_data(track_parts[1], track_parts[2]))

                # Nettoyage des track_datas
                track_data['title'], track_data['artist'], track_data['album'] = self.clean_track_elements(track_data['title'], track_data['artist'], track_data['album'])
                
                # Artwork
                if filename.endswith(('.aiff', '.m4a')):
                    track_data['artwork_path'] = None
                else:
                    track_data['artwork_path'] = os.path.abspath(self.dl_artwork(track_data['title'], track_data['artist'], track_data['artwork_url']))
                
                del track_data['artwork_url']

                self.added_db[iTunes_track_ID] = track_data  # Ajout de l'ID et des informations de la track au dictionnaire

                print(f"Track : {track_data['title']} - {track_data['artist']} ajoutée \n")
            


    def clean_track_elements(self, title, artist, album):
        '''
        Nettoie le titre, l'artiste et l'album

        Args: 
            - le titre
            - l'artiste
            - l'album

        Return:
            - le titre nettoyé
            - l'artiste nettoyé
            - l'album nettoyé
        '''
        #########
        # Titre #
        #########
        title = re.sub(r'- ([\p{L}0-9\s\'&]+(?: Remix| Mix))', r'(\1)', title)  # Met en forme la partie Remix / Mix
        title = re.sub(r'- (Extended Mix)', r'(\1)', title)  # Met en forme le Extended Mix
        title = re.sub(r'- (Radio Edit)', r'(\1)', title)  # Met en forme le Extended Mix
        title = re.sub(r'- (Official [^\)]+ Anthem)', r'(\1)', title)  # Met en forme le Official ... Anthem

        clean_feat = lambda s: (re.search(r'\(feat\. ([^\)]+)\)', s).group(1) if re.search(r'\(feat\. ([^\)]+)\)', s) else '', re.sub(r' \(feat\. ([^\)]+)\)', '', s).strip())  # Récupère le nom de l'artiste en feat puis supprime la partie feat
        feat_artist, title = clean_feat(title)
        title = (lambda title: title if title.istitle() else title.title())(title)  # Vérifie que chaque mot possède une majuscule


        ##########
        # Artist #
        ##########
        artists_list = [artist.strip() for artist in artist.split(',')]
        
        # Suppression de l'artiste de feat s'il existe
        if feat_artist != '':
            for artist in artists_list:
                if artist in feat_artist:
                    artists_list.remove(artist)
        # Suppresion du/des artiste(s) de remix
        remix_artist = re.search(r'((?:\()[\p{L}0-9\s\'&]+(?: Remix))', title).group(1) if re.search(r'((?:\()[\p{L}0-9\s\'&]+(?: Remix))', title) else ''
        if remix_artist != '':
            for artist in artists_list:
                if artist in remix_artist:
                    artists_list.remove(artist)

        artist = ' x '.join(artists_list)  # Reconstruction de la chaine de caractère 'artist'
        
        # Ajoute l'artiste en feat s'il existe
        if feat_artist != '':
            artist += f' ft. {feat_artist}'


        #########
        # Album #
        #########
        album = album.strip()

        # Supprime l'album si il est identique au titre
        if album.lower() == title.lower():
            album = ''

        return title, artist, album



    def dl_artwork(self, title, artist, artwork_url):
        ''' Télécharge l'artwork '''
        artwork_path = f'ressources/artwork/{title}-{artist}.jpg'

        # Téléchargement et enregistrement de l'artwork
        response = requests.get(artwork_url)

        if response.status_code == 200:  # Check if the request was successful
            with open(artwork_path, "wb") as file:
                file.write(response.content)
            print(f"Image successfully downloaded and saved as {artwork_url}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")

        return artwork_path     



    def get_abs_path(file_path):
        ''' Retourne le chemin absolu du fichier '''
        os.path.abspath(file_path)



    def remove_artwork(self, iTunes_track_ID):
        '''
        Supprime l'artwork
        '''
        artwork_path = self.added_db[iTunes_track_ID]['artwork_path']
        
        if artwork_path:
            os.remove(artwork_path)
            print(f"Fichier '{artwork_path}' supprimé avec succès.")
        else:
            print(f"Pas d'artwork a supprimer pour cette track")



    def rename_tracks(self): 
        '''
        Itère sur les éléments du dictionnaire et renomme les photos
        '''
        renamer = TrackRenamer()

        for iTunes_track_ID in self.added_db:  # Itération sur les éléments du dictionnaire
            track_data = self.added_db[iTunes_track_ID]

            release_year = track_data['release_year']  # Année de sortie
            title = track_data['title']  # Titre
            artist = track_data['artist']  # Artiste
            album = track_data['album']  # Album
            IDs = str(iTunes_track_ID) + ' ⎪ ' + track_data['spotify_id']  # ID iTunes & Spotify
            artwork_path = track_data['artwork_path']  # Artwork Path
            
            if title == 'Liminal':
                print(f'artist : {artist}')
                print(f'album : {album}')
                print(f'IDs : {IDs}')
                print(f'Artwork path : {artwork_path}')

            renamer.set_values(iTunes_track_ID, title, artist, album, release_year, IDs, artwork_path)  # Fixe les valeurs des attributs du TrackRenamer
            renamer.rename_track()  # Renommage de la track

            self.remove_artwork(iTunes_track_ID)# Suppression de l'artwork 


