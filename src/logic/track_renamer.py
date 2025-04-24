from src.config.logger_config import get_logger
import subprocess

class TrackRenamer():
    """
    A class to rename tracks in the Apple Music application using AppleScript.

    - Allows setting metadata such as title, artist, album, release year, and artwork.
    - Executes AppleScript commands to update track information in Apple Music.
    """
    def __init__(self):
        """
        Initializes the TrackRenamer instance.
        """
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
        """
        Sets the metadata values for the track to be renamed.

        Args:
            iTunes_ID (str): The persistent ID of the track in Apple Music.
            title (str): The new title of the track.
            artist (str): The new artist of the track.
            album (str): The new album of the track.
            release_year (int): The release year of the track.
            IDs (str): Additional identifiers to set in the track's comment field.
            artwork_path (str): The file path to the artwork image for the track.
        """
        self.iTunes_ID = iTunes_ID
        self.title = title
        self.artist = artist
        self.album = album
        self.release_year = int(release_year)
        self.IDs = IDs
        self.artwork_path = artwork_path

    def rename_track(self):
        """
        Renames the track in Apple Music using AppleScript.

        - Updates the track's metadata such as title, artist, album, release year, and comment.
        - Optionally updates the track's artwork if a valid file path is provided.
        """
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
