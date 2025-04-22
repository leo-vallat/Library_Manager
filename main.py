from src.logic.LibraryManager import LibraryManager
from src.logic.PlaylistManager import PlaylistManager
import time

if __name__ == '__main__':
    lbManager = LibraryManager() 
    
    ############################################################################################### 
    ## Ajouter des musiques à la bibliothèque                                                    ##
    ###############################################################################################
    lbManager.add_tracks()
    
    # time.sleep(1)  # Temporaire mais faut comprendre pourquoi y'a besoin de cette seconde, sinon erreur Applescript -50 (uniquement si 1 seule musique est ajoutée)

    lbManager.rename_tracks()




    ############################################################################################### 
    ## Mettre à jour les playlists de style                                                      ##
    ## Attention si mode 'Full' : pensez à vider les playlists avant de lancer le code           ##
    ###############################################################################################

    # plManager = PlaylistManager()

    # plManager.update_genre_playlist('Full', ["Euphoric Hardstyle", 'Hardstyle', 'Rawphoric', 'Frenchcore', 'Rawstyle'])