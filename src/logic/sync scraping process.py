import time
import random
import requests
from playwright.sync_api import sync_playwright

def bypass_cloudflare():
    user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SAMSUNG SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/17.0 Chrome/92.0.4515.166 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.99 Mobile Safari/537.36 OPR/65.2.2254.64137"
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True for no GUI
        context = browser.new_context()
        page = context.new_page()

        first_time = True
        second_time = False
        urls = ['https://tunebat.com/Info/Fire-D-Block-S-te-Fan/5Oh48t8W8xH1GTZ6fa6502', 'https://tunebat.com/Info/Find-The-Answer-Brennan-Heart-Toneshifterz/2NYsXmDeHFi2o3MTvzNsDb']

        for url in urls:
            start_time = time.time()

            page.set_extra_http_headers({"User-Agent": random.choice(user_agents)})  # Choisi un user-agent aléatoirement

            page.goto(url, timeout=60000)  # Navigue jusquà la page

            time.sleep(random_delay())
            
            if second_time:
                time.sleep(10000)

            if first_time:
                try:
                    # Wait for the "Continuer sans accepter" button and click it
                    button_selector = "button:has-text('Continuer sans accepter')"
                    page.wait_for_selector(button_selector, timeout=10000)
                    page.click(button_selector)
                    print("Cookie popup handled: 'Continuer sans accepter' clicked.")
                except Exception as e:
                    print("Error handling cookie popup:", e)
                first_time = False
                second_time = True
            

            """
            captcha_selector = "div#captcha-element"  # Replace with the actual CAPTCHA element selector
            if page.query_selector(captcha_selector):
                print("CAPTCHA detected. Please solve it manually...")
                while page.query_selector(captcha_selector):
                    # Wait for the CAPTCHA to disappear
                    print("Waiting for CAPTCHA resolution...")
                    page.wait_for_timeout(3000)  # Check every 3 seconds

                print("CAPTCHA resolved. Continuing with the script...")
            """

            # Wait for the Cloudflare challenge to complete
            page.wait_for_selector("body", timeout=10000)  # Adjust selector as needed

            first_line_elements = page.locator('.yIPfN')
            first_line_values = first_line_elements.all_inner_texts()


            second_line_elements = page.locator('.ant-progress-text')
            second_line_values = second_line_elements.all_inner_texts()


            print(first_line_values, '\n')
            print(second_line_values, '\n')

            time.sleep(random_delay())

            print(f'Temps de scraping : {time.time() - start_time:.2f} sec')



def random_delay():
    '''
    retourne une valeur aléatoire entre 0 et 5
    '''
    time = random.random() * 5
    print(f"Temps d'attente : {time} sec")
    return time



def login_to_popup():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)  # Set headless=False for manual debugging
        page = browser.new_page()

        # Navigate to the target website
        page.goto("https://tunebat.com")

        time.sleep(random_delay())

        try:
            # Wait for the "Continuer sans accepter" button and click it
            button_selector = "button:has-text('Continuer sans accepter')"
            page.wait_for_selector(button_selector, timeout=10000)
            page.click(button_selector)
            print("Cookie popup handled: 'Continuer sans accepter' clicked.")
        except Exception as e:
            print("Error handling cookie popup:", e)

        time.sleep(random_delay())

        # Wait for the page to load
        page.wait_for_load_state("load")

        # Step 1: Click the "Log In" button to open the popup
        #login_button_selector = "button.ant-btn"  # Selector for the "Log In" button
        login_button_selector = "button:has-text('Log In')"
        page.click(login_button_selector)
        print("Login popup opened.")
        
        time.sleep(random_delay())

        # Step 2: Fill in the email address and password
        email_selector = "input#email"  # Selector for the email input field
        password_selector = "input#password"  # Selector for the password input field
        page.fill(email_selector, "vanoise2002@gmail.com")  # Replace with your email
        page.fill(password_selector, "hUntox-munjig-guwpe9")  # Replace with your password

        print("Filled in email and password.")

        time.sleep(random_delay())

        # Step 3: Submit the login form
        submit_button_selector = "button#server-errors"  # Selector for the "Log In" button in the popup
        #submit_button_selector = "button:has-text('Log In')"
        page.click(submit_button_selector)

        time.sleep(random_delay())

        # Wait for the login to complete and the popup to close
        #page.wait_for_selector("div.ant-modal-content", state="detached")
        print("Login successful!")

        # Step 4: Perform post-login actions
        # Example: Navigate to another page or scrape data
        page.goto("https://tunebat.com/Info/Fire-D-Block-S-te-Fan/5Oh48t8W8xH1GTZ6fa6502")  # Replace with a protected URL
        
        time.sleep(100)
        print("Navigated to a protected page.")



def search_with_playwright():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)  # Set headless=True to run without UI
        page = browser.new_page()

        # Navigate to the website
        page.goto("https://tunebat.com")  # Replace with your target website
        
        time.sleep(random_delay())

        try:
            # Wait for the "Continuer sans accepter" button and click it
            button_selector = "button:has-text('Continuer sans accepter')"
            page.wait_for_selector(button_selector, timeout=10000)
            page.click(button_selector)
            print("Cookie popup handled: 'Continuer sans accepter' clicked.")
        except Exception as e:
            print("Error handling cookie popup:", e)

        # Locate the search bar and type text
        search_bar_selector = "input[aria-label='Song search field']"  # Update with the actual selector of the search bar
        page.fill(search_bar_selector, "Fire D-Block & S-Te-Fan")  # Replace with your search term

        # Submit the search (press Enter or click the search button)
        page.press(search_bar_selector, "Enter")  # Simulate pressing Enter key

        # Alternatively, if there's a "Search" button:
        # page.click("button[type='submit']")  # Update with the actual button selector

        # Wait for search results to load
        page.wait_for_load_state("load")
        print('Search successful !')
        
        time.sleep(100)
        '''
        # Extract search results or navigate further
        results_selector = ".result-class"  # Update with the actual selector for results
        results = page.query_selector_all(results_selector)

        # Print the results (example: extract text from result elements)
        for result in results:
            print(result.inner_text())

        # Close the browser
        browser.close()
        '''

#bypass_cloudflare()
#login_to_popup()
search_with_playwright()