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

    # library.playlists.update_genre_playlist('Full', ["Euphoric Hardstyle", 'Hardstyle', 'Techno', 'Hard Techno', 'Trance', 'Hard Trance', 'Rawphoric', 'Drum and Bass'])

    library.playlists.manage('MUSCU', 100, ['Hardstyle', 'Rawstyle', 'Frenchcore'])

    library.playlists.manage('EUPHORIC', 200, ['Euphoric Hardstyle', 'Rawphoric', 'Happy Hardcore', 'Frenchcore', 'Drum and Bass'])

    # library.playlists.restore_history('Gland')