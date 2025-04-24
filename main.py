from src.library_manager import LibraryManager
import time

if __name__ == '__main__':
    lbManager = LibraryManager() 
    
    ############################################################################################### 
    ## Ajouter des musiques à la bibliothèque                                                    ##
    ###############################################################################################
    # lbManager.add_tracks()

    ############################################################################################### 
    ## Mettre à jour les playlists de style                                                      ##
    ###############################################################################################

    lbManager.playlists.update_genre_playlist('Full', ["Euphoric Hardstyle", 'Hardstyle', 'pap'])
    lbManager.playlists.create_playlist('test')