import subprocess

class TrackRenamer():
    def __init__(self):
        self.iTunes_ID = None
        self.title = None
        self.artist = None
        self.album = None
        self.release_year = None
        self.bpm = None
        self.key = None
        self.energy = None
        self.happiness = None
        self.danceability = None
        self.loudness = None
        self.speechiness = None
        self.IDs = None
        self.artwork_path = None

    def set_values(self, iTunes_ID, title, artist, album, release_year, bpm, key, energy, happiness, danceability, loudness, speechiness,IDs, artwork_path):
        '''
        Modifie les valeurs des attributs avec les valeurs passées en paramètres
        '''
        self.iTunes_ID = iTunes_ID
        self.title = title
        self.artist = artist
        self.album = album
        self.release_year = release_year
        self.bpm = bpm
        self.key = key
        self.energy = energy
        self.happiness = happiness
        self.danceability = danceability
        self.loudness = loudness
        self.speechiness = speechiness
        self.IDs = IDs
        self.artwork_path = artwork_path


    def rename_track(self):

        # Commande AppleScript
        command = [
        'osascript', 
        '-e', 'tell application "Music"', 
        '-e', f'set theTrack to (first track whose persistent ID is "{self.iTunes_ID}")', 
        '-e', f'set name of theTrack to "{self.title}"',
        '-e', f'set artist of theTrack to "{self.artist}"'
        ]

        if self.album:
            command.append('-e')
            command.append(f'set album of theTrack to "{self.album}"')
        
        if self.release_year:
            self.release_year = int(self.release_year)
            command.append('-e')
            command.append(f'set year of theTrack to {self.release_year}')
        
        if self.bpm:
            self.bpm = int(self.bpm)
            command.append('-e')
            command.append(f'set bpm of theTrack to {self.bpm}')

        if self.key:
            command.append('-e')
            command.append(f'set grouping of theTrack to "{self.key}"')

        if self.energy:
            command.append('-e')
            command.append(f'set rating of theTrack to {self.energy}')

        if self.happiness:
            self.happiness = int(self.happiness)
            command.append('-e')
            command.append(f'set track number of theTrack to {self.happiness}')

        if self.danceability:
            self.danceability = int(self.danceability)
            command.append('-e')
            command.append(f'set disc number of theTrack to {self.danceability}')

        if self.loudness:
            command.append('-e')
            command.append(f'set category of theTrack to "{self.loudness}"')

        if self.speechiness:
            command.append('-e')
            command.append(f'set description of theTrack to "{self.speechiness}"')

        if self.IDs:
            command.append('-e')
            command.append(f'set comment of theTrack to "{self.IDs}"')
        
        if self.artwork_path:
            command.append('-e')
            command.append(f'set artworkData to read (POSIX file "{self.artwork_path}") as JPEG picture')
            command.append('-e')
            command.append('set data of artwork 1 of theTrack to artworkData')

        command.append('-e')
        command.append('end tell')

        # Exécution de la commande via subprocess
        result = subprocess.run(command, capture_output=True, text=True)

        # Vérification des erreurs
        if result.returncode != 0:
            print(f"\nErreur lors de l'exécution d'AppleScript : {result.stderr}")
            print(self.title)
            print(self.iTunes_ID)
            print('---------------------------------------------------------\n')
        else:
            print(f"Track : {self.title} renommée avec succès.")

