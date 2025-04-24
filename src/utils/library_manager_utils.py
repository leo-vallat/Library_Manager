from src.config.config import AppConfig, CleaningRules
from src.logic.spotify_data_getter import SpotifyDataGetter
import regex as re
from src.config.logger_config import get_logger
import os
import requests
import subprocess

logger = get_logger(__name__)

def get_batch_id():
    """
    Reads the current batch ID from a file, increments it, and saves the updated value.

    Returns:
        int: The new batch ID.
    """
    with open(AppConfig.BATCH_ID_FILE_PATH, "r") as f:
        batch_id = int(f.read().strip())
    batch_id += 1
    with open(AppConfig.BATCH_ID_FILE_PATH, "w") as f:
        f.write(str(batch_id))
    return batch_id

def add_track(track_path):
    """
    Adds a track to the Apple Music library.

    Args:
        track_path (str): The file path of the track to add.

    Returns:
        subprocess.CompletedProcess: The result of the subprocess call.
    """
    return subprocess.run(['open', '-a', 'Music', track_path], capture_output=True, text=True)

def format_track_data(filename):
    """
    Formats track metadata based on the filename and retrieves additional data from Spotify.

    Args:
        filename (str): The name of the track file.

    Returns:
        dict: A dictionary containing track metadata, including title, artist, album, release year, Spotify ID, and artwork path.
    """
    spotify = SpotifyDataGetter()

    # Split the parts of the track
    if filename.endswith('.aiff'):
        track_parts = filename[:-5].split('%')
    else:
        track_parts = filename[:-4].split('%')  

    # Add parts if necessary
    while len(track_parts) < 4 :
        track_parts.append('')
    
    track_data = {'release_year' : track_parts[0], 'title' : track_parts[1], 'artist' : track_parts[2], 'album' : track_parts[3]}

    # Add spotify and artwork url
    track_data.update(spotify.get_track_data(track_parts[1], track_parts[2]))

    # Clean track_data
    track_data['title'], track_data['artist'], track_data['album'] = _clean_track_elements(track_data['title'], track_data['artist'], track_data['album'])
    
    # Artwork
    if filename.endswith(('.aiff', '.m4a')):
        track_data['artwork_path'] = None
    else:
        track_data['artwork_path'] = os.path.abspath(_dl_artwork(track_data['title'], track_data['artist'], track_data['artwork_url']))
    del track_data['artwork_url']

    return track_data

def _clean_track_elements(title, artist, album):
    """
    Cleans the title, artist, and album strings.

    Args:
        title (str): The track's title.
        artist (str): The track's artist.
        album (str): The track's album.

    Returns:
        tuple: Cleaned title, artist, and album strings.
    """
    title, feat_artist = _clean_title(title)
    artist = _clean_artist(artist, title, feat_artist)
    album = _clean_album(album, title)
    return title, artist, album

def _clean_title(title):
    """
    Cleans the title string and extracts featured artists.

    Args:
        title (str): The track's title.

    Returns:
        tuple: The cleaned title and the featured artist(s).
    """
    title = _remove_unwanted_patterns(title, 'title')
    # Shapes suffixes
    title = re.sub(r'- ([\p{L}0-9\s\'&\-]+(?: Remix| Mix| Edit| Anthem| OST| Official Soundtrack))', r'(\1)', title)  

    # Get and remove the 'feat.'
    feat_artist_match = re.search(r'\(feat\. ([^\)]+)\)', title)
    feat_artist = feat_artist_match.group(1) if feat_artist_match else ''
    title = re.sub(r' \(feat\. ([^\)]+)\)', '', title).strip()

    return title, feat_artist

def _clean_artist(artist, title, feat_artist):
    """
    Cleans the artist string and removes unnecessary elements.

    Args:
        artist (str): The track's artist.
        title (str): The track's title.
        feat_artist (str): The featured artist(s).

    Returns:
        str: The cleaned artist string.
    """
    artist = _remove_unwanted_patterns(artist, 'artist')

    artists_list = [a.strip() for a in artist.split(',') if a]
    
    # Remove feat artists
    if feat_artist:
        artists_list = [a for a in artists_list if a not in feat_artist]
    
    # Suppresion du/des artiste(s) de remix
    remix_artist_match = re.search(r'((?:\()[\p{L}0-9\s\'&\-]+(?: Remix))', title)
    remix_artist = remix_artist_match.group(1) if remix_artist_match else ''

    if remix_artist:
        artists_list = [a for a in artists_list if a not in remix_artist]
    cleaned_artist = ', '.join(artists_list)
    
    # Ajoute l'artiste en feat s'il existe
    if feat_artist:
        cleaned_artist += f' ft. {feat_artist}'

    return cleaned_artist

def _clean_album(album, title):
    """
    Cleans the album string and removes unnecessary elements.

    Args:
        album (str): The track's album.
        title (str): The track's title.

    Returns:
        str: The cleaned album string.
    """
    album = _remove_unwanted_patterns(album, 'album')
    album = album.strip()
    # Deletes album if identical to title
    if album.lower() == title.lower():
        album = ''
    return album

def _remove_unwanted_patterns(text, field):
    """
    Removes unwanted patterns from a string based on predefined rules.

    Args:
        text (str): The text to clean.
        field (str): The field type ('title', 'artist', or 'album').

    Returns:
        str: The cleaned text.
    """
    field_rules = getattr(CleaningRules, field.upper(), [])
    patterns = field_rules + CleaningRules.GLOBAL
    for pattern in patterns:
        text = text.replace(pattern, '')
    return text.strip()

def _dl_artwork(title, artist, artwork_url):
    """
    Downloads the artwork for a track.

    Args:
        title (str): The track's title.
        artist (str): The track's artist.
        artwork_url (str): The URL of the artwork.

    Returns:
        str: The file path to the downloaded artwork.
    """
    artwork_path = f'ressources/artwork/{title}-{artist}.jpg'
    logger.debug(f"Download artwork from: {artwork_url}")
    response = requests.get(artwork_url)
    if response.status_code == 200:
        with open(artwork_path, "wb") as file:
            file.write(response.content)
    else:
        logger.warning(f"❌ Failed to download artwork. Status code: {response.status_code}")
        artwork_path = None
    return artwork_path 