from src.library_manager import LibraryManager
import time

if __name__ == '__main__':
    library = LibraryManager() 
    
    ############################################################################################### 
    ## Ajouter des musiques à la bibliothèque                                                    ##
    ###############################################################################################
    # library.add_tracks()

    ############################################################################################### 
    ## Mettre à jour les playlists de style                                                      ##
    ###############################################################################################

    # library.playlists.update_genre_playlist('Full', ["Euphoric Hardstyle", 'Hardstyle', 'pap'])
    # library.playlists.create_playlist('test')
    library.playlists.manage('TEST 2', 5, ['Euphoric Hardstyle', 'Hardstyle'], include_recent=True)