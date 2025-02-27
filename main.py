from src.logic.LibraryManager import LibraryManager
import time

if __name__ == '__main__':
    manager = LibraryManager() 
    
    ############################################################################################### 
    ## Ajouter des musiques à la bibliothèque                                                    ##
    ###############################################################################################
    manager.add_tracks()
    
    # time.sleep(1)  # Temporaire mais faut comprendre pourquoi y'a besoin de cette seconde, sinon erreur Applescript -50 (uniquement si 1 seule musique est ajoutée)

    manager.rename_tracks()




    ############################################################################################### 
    ## Mettre à jour les playlists de style                                                      ##
    ###############################################################################################
