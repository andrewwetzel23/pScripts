from systemFuncs import browseForDir

import os
from glob import glob
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

"""

This program was intended to have the user browse for folder, and then 
convert every html file in that folder into a jpg from as screenshot of
the html in the browser.

Doesn't currently load all of the javascript code. Button text and other
dynamically loaded content is not loaded.


"""

def convert_html_to_jpg(directory, screen_size=(1280, 800)):
    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set the window size
    chrome_options.add_argument(f"--window-size={screen_size[0]},{screen_size[1]}")

    # Set up WebDriver
    webdriver_service = Service(ChromeDriverManager().install())

    os.chdir(directory)

    # Convert each HTML file in the directory
    for html_file in glob("*.html"):
        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
        
        # Open the HTML file in Chrome
        driver.get(f"file://{os.getcwd()}/{html_file}")

        # Take screenshot
        driver.save_screenshot(html_file.replace('.html', '.jpg'))

        # Quit the browser
        driver.quit()


# Use the function
convert_html_to_jpg(browseForDir())
