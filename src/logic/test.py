import time
from playwright.sync_api import sync_playwright

def bypass_cloudflare():
    start_time = time.time()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True for no GUI
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the target website
        page.goto("https://tunebat.com/Info/How-Deep-Is-Your-Love-Calvin-Harris-Disciples/22mek4IiqubGD9ctzxc69s", timeout=60000)

        #time.sleep(10)
        
        try:
            # Wait for the "Continuer sans accepter" button and click it
            button_selector = "button:has-text('Continuer sans accepter')"
            page.wait_for_selector(button_selector, timeout=10000)
            page.click(button_selector)
            print("Cookie popup handled: 'Continuer sans accepter' clicked.")
        except Exception as e:
            print("Error handling cookie popup:", e)

        
        # Wait for the Cloudflare challenge to complete
        page.wait_for_selector("body", timeout=10000)  # Adjust selector as needed

        first_line_elements = page.locator('.yIPfN')
        first_line_values = first_line_elements.all_inner_texts()


        second_line_elements = page.locator('.ant-progress-text')
        second_line_values = second_line_elements.all_inner_texts()


        print(first_line_values, '\n')
        print(second_line_values, '\n')
        # Close the browser
        #browser.close()

        print(f'{time.time() - start_time:.2f}')
bypass_cloudflare()
