import random
import asyncio
from playwright.async_api import async_playwright

###################################################################################################
# Processus de scraping asynchrone et semi automatique 
# Navigue sur la page principale de Tunebat
# Décline les cookies
# Boucle sur l'ensemble la liste des tracks
# Recherche la track 
# Attend le clique de l'utilisateur sur la bonne track
# Détecte la page de la track et récupère les données intéressantes
# Recherche la track suivante et ainsi de suite
#
# Problème : La recherche est peu effective et aléatoire, malgré le nom de la track 
# et artiste identique 
#
# Cause potentielle : le moteur de recherche est guez, le site détecte le scraping / 
# utilisation de code et affiche délibérement aucune données
###################################################################################################

async def navigate_to_site(page):
    """
    Navigate to the main site
    """
    await page.goto("https://tunebat.com")
    await page.wait_for_load_state("domcontentloaded")
    
    # Bloque pour refuser les cookies
    try:
        # Wait for the "Continuer sans accepter" button and click it
        button_selector = "button:has-text('Continuer sans accepter')"
        await page.wait_for_selector(button_selector, timeout=10000)
        await page.click(button_selector)
        print("Cookie popup handled: 'Continuer sans accepter' clicked.")
    except Exception as e:
        print("Error handling cookie popup:", e)



async def search_for_track(page, track_name):
    """
    Search for a track using the search bar
    """
    search_selector = 'input[aria-label="Song search field"]'
    await page.wait_for_selector(search_selector)
    await page.fill(search_selector, track_name)
    await page.keyboard.press("Enter")  # Simulate pressing Enter
    await detect_page(page, "Search")



async def detect_page(page, page_type):
    """
    Wait for a specific page to load
    """
    if page_type=='Search':
        page_selector = "button:has-text('Search')"
    elif page_type=='Track':
        page_selector = "button[aria-label='Share this page']"
    
    try:
        await page.wait_for_selector(page_selector)
        print(f"{page_type} page detected")

    except Exception as e:
        print(f"Error while trying detecting page : {e}")



async def wait_for_manual_click(page):
    print("Please manually select the desired track from the search results...")
    await detect_page(page, "Track")



async def scrape_data(page):
    """
    Scrape data from the current track's page
    """
    await page.wait_for_load_state("domcontentloaded")
    
    first_line_elements = page.locator('.yIPfN')
    first_line_values = await first_line_elements.all_inner_texts()

    second_line_elements = page.locator('.ant-progress-text')
    second_line_values = await second_line_elements.all_inner_texts()

    return {"first line": first_line_values, "second line": second_line_values}



def random_delay():
    '''
    retourne une valeur aléatoire entre 0 et 5
    '''
    time = random.random() * 5
    print(f"Temps d'attente : {time} sec")
    return time




async def process_tracks(tracks):
    """
    Process each track: search, wait for click, scrape data
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Headful mode for manual interaction
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navigate to the main site
        await navigate_to_site(page)

        results = []
        for track in tracks:
            print(f"Processing track: {track}")
            
            random_delay()

            # Step 1: Search for the track
            await search_for_track(page, track)
            
            # Step 2: Wait for the user to click the correct result
            await wait_for_manual_click(page)
            
            # Step 3: Scrape the data
            data = await scrape_data(page)
            results.append(data)
                    
        await browser.close()
        return results



# Run the script
tracks_to_scrape = ["Escape Me From Fall Synapse", "Hollow Wildstylez, Atmozfears", "Dragonborn - Original Mix Headhunterz"]  # Replace with your actual tracks
results = asyncio.run(process_tracks(tracks_to_scrape))

# Print results
print("Scraped Data:")
for result in results:
    print(result)
