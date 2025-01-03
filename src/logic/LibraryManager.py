from ScriptingBridge import SBApplication
from TrackRenamer import TrackRenamer
from SpotifyDataGetter import SpotifyDataGetter
from dotenv import load_dotenv
import os
import subprocess
import time
import regex as re


class LibraryManager(): 
    def __init__(self):
        """
        Constructeur du manager de bibliothèque
        """
        load_dotenv('../../.env')
        self.music_app = SBApplication.applicationWithBundleIdentifier_("com.apple.Music")  # Connexion à Musique
        self.library_path = os.getenv('LIBRARY_PATH')  # Chemin vers la bibliothèque
        self.test_library_path = os.getenv('TEST_LIBRARY_PATH')  # Chemin vers la bibliothèque
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

    def get_track_count(self):
        '''
        Retourne le nombre de track de la bibliothèque
        '''
        return len(self.music_app.tracks())



    def add_musics(self):
        '''
        Déplace les musiques du dossier de téléchargement vers le dossier d'ajout à Musique. 
        '''
        spotify = SpotifyDataGetter()
        for filename in os.listdir(self.downloaded_music_path):
            if filename.endswith(('.mp3', '.wav', '.aac', '.flac')):
                music_path = os.path.join(self.downloaded_music_path, filename)
                                
                subprocess.run(['open', '-a', 'Music', music_path])  # Ajout de la track à la bibliothèque

                time.sleep(1)  # Attente que la track soit ajoutée à la bibliothèque

                track = self.get_last_added_track()  # Récupération de la track ajoutée
                iTunes_track_ID = track.persistentID()  # ID attribuée à la track dans Musique

                track_parts = filename[:-4].split('%')  # Séparation du nom de la track

                #  Vérification qu'il y ait bien 4 parties différentes (sinon la partie est créée et vaut '')
                while len(track_parts) < 4 :
                    track_parts.append('')
                
                #  Ajout des valeurs bpm, clé et énergie à la liste 
                track_data = spotify.get_track_data(track_parts[1], track_parts[2])
                track_parts.append(track_data['BPM'])
                track_parts.append(track_data['key'])
                track_parts.append(track_data['energy'])
                track_parts.append(track_data['happiness'])
                track_parts.append(track_data['danceability'])
                track_parts.append(track_data['loudness'])
                track_parts.append(track_data['speechiness'])
                track_parts.append(track_data['spotify_id'])

                track_parts[1], track_parts[2], track_parts[3] = self.clean_track(track_parts[1], track_parts[2], track_parts[3])  # Nettoyage des différentes parties
                self.added_db[iTunes_track_ID] = track_parts  # Ajout de l'ID et des informations de la track au dictionnaire

                print(f"Track : {track_parts[1]} - {track_parts[2]} ajoutée")

    

    def clean_track(self, title, artist, album):
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
        artists_list = artist.split(',')  # Séparation des différents artistes
        artists_list = [artist.strip() for artist in artists_list]  # Suppression des espaces inutiles
        
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

        artist = ' x '.join(artists_list)  # Reconstruction de la chaine de caractère artist
        
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



    def rename_musics(self): 
        '''
        Itère sur les éléments du dictionnaire et renomme les photos
        '''
        renamer = TrackRenamer()

        for iTunes_track_ID in self.added_db:  # Itération sur les éléments du dictionnaire
            release_year = self.added_db[iTunes_track_ID][0]  # Année de sortie
            title = self.added_db[iTunes_track_ID][1]  # Titre
            artist = self.added_db[iTunes_track_ID][2]  # Artiste
            album = self.added_db[iTunes_track_ID][3]  # Album
            bpm = self.added_db[iTunes_track_ID][4]  # BPM
            key = self.added_db[iTunes_track_ID][5]  # Clé 
            energy = self.added_db[iTunes_track_ID][6]  # Énergie
            happiness = self.added_db[iTunes_track_ID][7]  # Positivité
            danceability = self.added_db[iTunes_track_ID][8]  # Dansabilité
            loudness = self.added_db[iTunes_track_ID][9]  # Niveau Sonore
            speechiness = self.added_db[iTunes_track_ID][10]  # A quel point il y a des paroles dans la musique
            IDs = str(iTunes_track_ID) + ' ⎪ ' + self.added_db[iTunes_track_ID][11]  # ID iTunes & Spotify


            renamer.set_values(iTunes_track_ID, title, artist, album, release_year, bpm, key, energy, happiness, danceability, loudness, speechiness, IDs)  # Fixe les valeurs des attributs du TrackRenamer
            renamer.rename_track()  # Renommage de la track