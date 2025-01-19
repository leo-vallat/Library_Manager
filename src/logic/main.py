from LibraryManager import LibraryManager
import time

if __name__ == '__main__':
    manager = LibraryManager() 
    
    manager.add_musics()
    
    time.sleep(1)  # Temporaire mais faut comprendre pourquoi y'a besoin de cette seconde, sinon erreur Applescript -50

    manager.rename_musics()