from src.config.logger_config import get_logger, log_session_start
import time

def main():
    logger = get_logger("TestLogger")
    log_session_start(logger)

    logger.info("🟢 Lancement du test du logger")
    
    # Simule des opérations avec différents niveaux
    logger.info("Ajout d'une track à la bibliothèque : Artist - Track A")
    time.sleep(0.5)

    logger.warning("Attention : le format du fichier n'est pas standard")
    time.sleep(0.5)

    logger.error("Erreur lors de la récupération des métadonnées depuis Spotify")
    time.sleep(0.5)

    logger.info("Ajout d'une track à la playlist : Chill Vibes")
    time.sleep(0.5)

    logger.warning("Artwork manquant pour la track suivante : Track B")
    time.sleep(0.5)

    logger.error("Impossible de supprimer le fichier temporaire : artwork_temp.jpg")
    time.sleep(0.5)

    logger.info("✅ Test du logger terminé avec succès.")

if __name__ == '__main__':
    main()