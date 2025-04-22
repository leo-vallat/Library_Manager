import regex as re

def get_batch_id():
    ''' Read batch_id.txt, update the value and save it '''
    batch_id_path = 'ressources/batch_id.txt'
    with open(batch_id_path, "r") as f:
        batch_id = int(f.read().strip())
    batch_id += 1
    with open(batch_id_path, "w") as f:
        f.write(str(batch_id))
    return batch_id

def clean_track_elements(title, artist, album):
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

    artist = ', '.join(artists_list)  # Reconstruction de la chaine de caractère 'artist'
    
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