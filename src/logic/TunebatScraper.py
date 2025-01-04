import urllib.parse





class TunebatScraper():
    def __init__(self):
        '''
        Constructeur du TunebatScraper
        '''




    def create_url(self, track_name, artists, spotify_id):
        '''
        Crée l'url vers les informations de la musique sur tunebat
        '''
        track_name = urllib.parse.quote(track_name.replace(" ", "-"))
        artists = urllib.parse.quote(artists.replace(", ", "-").replace(" ", "-"))

        url_base = 'https://tunebat.com/Info/'
        url = f"{url_base}{track_name}-{artists}/{spotify_id}"

        return url
    


    def scrap(self, track_name, artists, spotify_id):
        '''
        
        '''
        url = self.create_url(track_name, artists, spotify_id)




###################################################################################################
#  Exemple d'utilisation / Test
###################################################################################################
track_name = "Move"
artists = "Adam Port, Stryv, Keinemusik, Orso, Malachiii"
spotify_id = "1BJJbSX6muJVF2AK7uH1x4"


scraper = TunebatScraper()
scraper.scrap(track_name, artists, spotify_id)
###################################################################################################