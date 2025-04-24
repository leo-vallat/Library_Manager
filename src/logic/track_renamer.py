from src.config.logger_config import get_logger
import subprocess

class TrackRenamer():
    def __init__(self):
        self.iTunes_ID = None
        self.title = None
        self.artist = None
        self.album = None
        self.release_year = None
        self.IDs = None
        self.artwork_path = None
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('🟢 Track Renamer initialized')

    def set_values(self, iTunes_ID, title, artist, album, release_year, IDs, artwork_path):
        '''
        Modifie les valeurs des attributs avec les valeurs passées en paramètres
        '''
        self.iTunes_ID = iTunes_ID
        self.title = title
        self.artist = artist
        self.album = album
        self.release_year = int(release_year)
        self.IDs = IDs
        self.artwork_path = artwork_path

    def rename_track(self):
        self.logger.debug(f"Renaming {self.title} - {self.artist}")
        # Commande AppleScript
        command = [
        'osascript', 
        '-e', 'tell application "Music"', 
        '-e', f'set theTrack to (first track whose persistent ID is "{self.iTunes_ID}")', 
        '-e', f'set name of theTrack to "{self.title}"',
        '-e', f'set artist of theTrack to "{self.artist}"',
        '-e', f'set album of theTrack to "{self.album}"',
        '-e', f'set year of theTrack to {self.release_year}'
        ]
        
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
            self.logger.warning(f"❌ Applescript error while renaming the track {self.title} - {self.artist} → {result.stderr.strip()}")
