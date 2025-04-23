from src.config.config import AppConfig, CleaningRules
import regex as re

def get_batch_id():
    ''' Read batch_id.txt, update the value and save it '''
    with open(AppConfig.BATCH_ID_FILE_PATH, "r") as f:
        batch_id = int(f.read().strip())
    batch_id += 1
    with open(AppConfig.BATCH_ID_FILE_PATH, "w") as f:
        f.write(str(batch_id))
    return batch_id

def clean_track_elements(title, artist, album):
    '''
    Clean title, artist and album strings

    Args: 
        title (str): track's title
        artist (str): track's artist
        album (str): track's album
    '''
    title, feat_artist = _clean_title(title)
    artist = _clean_artist(artist, title, feat_artist)
    album = _clean_album(album, title)
    return title, artist, album

def _clean_title(title):
    title = _remove_unwanted_patterns(title, 'title')
    # Shapes suffixes
    title = re.sub(r'- ([\p{L}0-9\s\'&\-]+(?: Remix| Mix| Edit| Anthem| OST| Official Soundtrack))', r'(\1)', title)  

    # Get and remove the 'feat.'
    feat_artist_match = re.search(r'\(feat\. ([^\)]+)\)', title)
    feat_artist = feat_artist_match.group(1) if feat_artist_match else ''
    title = re.sub(r' \(feat\. ([^\)]+)\)', '', title).strip()

    return title, feat_artist

def _clean_artist(artist, title, feat_artist):
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
    album = _remove_unwanted_patterns(album, 'album')
    album = album.strip()
    # Deletes album if identical to title
    if album.lower() == title.lower():
        album = ''
    return album

def _remove_unwanted_patterns(text, field):
    '''
    Deletes patterns defined for a specific field + global rules.
    
    Args:
        text (str): text to clean
        field (str): 'title', 'artist' or 'album'
    
    Return:
        str: cleaned text
    '''
    field_rules = getattr(CleaningRules, field.upper(), [])
    patterns = field_rules + CleaningRules.GLOBAL
    for pattern in patterns:
        text = text.replace(pattern, '')
    return text.strip()