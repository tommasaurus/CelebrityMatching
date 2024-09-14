import random
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Set up the WebDriver
driver_path = '/Users/tommyqu/Downloads/chromedriver-mac-arm64/chromedriver'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Path to save images
images_folder = 'downloaded_onlyfans'
os.makedirs(images_folder, exist_ok=True)

# Headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scroll_to_bottom(driver, scroll_pause_time=1, scroll_increment=200):
    """Scroll down the webpage slowly to the bottom by checking document height."""
    while True:
        # Scroll down by the scroll increment
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        
        # Wait a bit to mimic human behavior
        time.sleep(scroll_pause_time)
        
        # Calculate the scroll position
        current_scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight;")
        max_scroll_height = driver.execute_script("return document.body.scrollHeight;")
        
        # Break the loop if we've reached the bottom
        if current_scroll_position >= max_scroll_height:
            break

def scrape_images(driver):
    # Wait for elements to load (modify the wait as needed)
    image_data = []

    try:
        # Locate all elements containing the images and names
        elements = driver.find_elements(By.CLASS_NAME, 'thumbshot')

        for element in elements:
            # Extract the <a> tag and get the title (name)            
            img_tag = element.find_element(By.TAG_NAME, 'img')
            name = img_tag.get_attribute('alt')
            name = name.replace("profile", "").replace("photo", "").strip()

            # Extract the image URL
            img_src = img_tag.get_attribute('src')
            img_url = f"https://www.babepedia.com{img_src}" if img_src.startswith('/') else img_src
            img_name = img_src.split('/')[-1]
            img_filepath = os.path.join(images_folder, img_name)
            
            print(f"Downloading image for {name}: {img_url}")

            try:
                # Download the image with headers
                response = requests.get(img_url, headers=headers)
                
                if response.status_code == 200:
                    # Save the image
                    with open(img_filepath, 'wb') as img_file:
                        img_file.write(response.content)
                    print(f"Saved: {img_filepath}")

                    # Add the file path and name to the list for CSV
                    image_data.append([img_filepath, name])
                else:
                    print(f"Failed to download image. Status code: {response.status_code}")
                

            except Exception as e:
                print(f"Error processing {name}: {e}")

    except Exception as e:
        print(f"An error occurred during scraping: {e}")

    return image_data

try:
    # Loop through the first 10 pages
    all_image_data = []
    for page_num in range(1, 11):  # Adjust range to specify the number of pages to scrape
        url = f'https://www.babepedia.com/onlyfanstop100?page={page_num}'
        print(f"Scraping page: {url}")
        
        # Open the webpage
        driver.get(url)
        scroll_to_bottom(driver, scroll_pause_time=0.5, scroll_increment=300)
        image_data = scrape_images(driver)
        
        # Add the image data from this page to the overall list
        all_image_data.extend(image_data)

    # Save all data to CSV
    if all_image_data:
        csv_path = 'onlyfans_data.csv'
        with open(csv_path, 'a') as csv_file:
            for row in all_image_data:
                csv_file.write(','.join(row) + '\n')
        print(f"Data saved to {csv_path}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    time.sleep(3)
    driver.quit()
