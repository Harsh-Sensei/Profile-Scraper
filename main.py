from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import os
import base64
import requests
from bs4 import BeautifulSoup


def create_folder(folder_name):
    """Create a folder if it doesn't exist."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def save_base64_image(base64_data, save_path):
    """Save image from base64 data."""
    try:
        # Remove the data URL prefix if present
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]
        
        # Decode and save the image
        image_data = base64.b64decode(base64_data)
        with open(save_path, "wb") as f:
            f.write(image_data)
        return True
    except Exception as e:
        print(f"Failed to save base64 image: {e}")
        return False

def fetch_images_with_selenium(query, base_folder, driver_path=None):
    """Fetch images using the exact HTML structure."""
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)
    driver.get("https://images.google.com/")
    for query in queries:
        try:
        # if True:
            # Open Google Images
            
            # Search for the query
            # Wait for the search box to be present
            search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            print(f"Searching for: {query}")
            time.sleep(2)

            # Scroll down to load more images

            # Create folder for the query
            folder_name = os.path.join(base_folder, query.replace(" ", "_"))
            create_folder(folder_name)

            # Find all div elements with class H8Rx8c
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.H8Rx8c")))
            h8rx8c_divs = driver.find_elements(By.CSS_SELECTOR, "div.H8Rx8c")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.EZAeBe")))
            EZAeBe_as = driver.find_elements(By.CSS_SELECTOR, "a.EZAeBe")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.JMWMJ")))
            desc_divs = driver.find_elements(By.CSS_SELECTOR, "div.JMWMJ")
            print(f"Found {len(h8rx8c_divs)} H8Rx8c divs")

            for i, div in enumerate(h8rx8c_divs[:3]):
                try:
                    desc = desc_divs[i].find_element(By.CSS_SELECTOR, "div.OSrXXb").text
                    # Find the g-img element within the div
                    g_img = div.find_element(By.TAG_NAME, "g-img")
                    print(f"Found g-img in div {i}")

                    # Find the img element within the g-img
                    img = g_img.find_element(By.TAG_NAME, "img")
                    print(f"Found img in g-img {i}")

                    # Get the src attribute
                    src = img.get_attribute("src")
                    print(f"Image {i} src: {src[:100]}...") # Print first 100 chars of src

                    # Save the image
                    image_save_path = os.path.join(folder_name, f"image_{i}.png")
                    if save_base64_image(src, image_save_path):
                        print(f"Successfully saved image {i}")
                    else:
                        print(f"Failed to save image {i}")
                        
                    # scrape the website from url
                    url = EZAeBe_as[i].get_attribute("href")
                    print(f"URL: {url}")
                    
                    response = requests.get(url,timeout=10)
                    soup = BeautifulSoup(response.content, "html.parser")
                    html_text = soup.get_text()
                    print(f"HTML Text: {html_text[:100]}...")
                    
                    # Save the HTML
                    html_save_path = os.path.join(folder_name, f"data_{i}.html")
                    with open(html_save_path, "w", encoding="utf-8") as f:
                        f.write(desc + "\n\n\n" + "url: " + url + "\n" + html_text)
                except Exception as e:
                    print(f"Error processing div {i}: {e}")

            # Close the browser
        except Exception as e:
            print(f"Error processing query {query}: {e}")
    driver.quit()

# Define queries and base folder
with open("names.txt", "r") as f:
    queries = [elem.strip("\n") + " Urologist" for elem in f.readlines()]  # Reduced to single query for testing"
queries = [query.strip() for query in queries]
print(queries)
base_folder = "selenium_search_results"

# Create base folder
create_folder(base_folder)

# Fetch and save results for each query

fetch_images_with_selenium(queries[0], base_folder, driver_path=r"chromedriver-win64\chromedriver-win64\chromedriver.exe")