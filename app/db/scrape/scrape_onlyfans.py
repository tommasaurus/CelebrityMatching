import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, unquote
import random
import csv

# Set up the WebDriver
driver_path = '/Users/tommyqu/Downloads/chromedriver-mac-arm64/chromedriver'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Path to save images
images_folder = 'app/db/images/images_onlyfans'
os.makedirs(images_folder, exist_ok=True)

# Headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scroll_to_bottom(driver, scroll_pause_time=1, scroll_increment=200):
    """Scroll down the webpage slowly to the bottom by checking document height."""
    while True:
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(scroll_pause_time)
        
        current_scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight;")
        max_scroll_height = driver.execute_script("return document.body.scrollHeight;")
        
        if current_scroll_position >= max_scroll_height:
            break

def scroll_to_top(driver, scroll_pause_time=1, scroll_increment=200):
    """Scroll up the webpage slowly to the top by checking scroll position."""
    while True:
        driver.execute_script(f"window.scrollBy(0, -{scroll_increment});")
        time.sleep(scroll_pause_time)
        
        current_scroll_position = driver.execute_script("return window.pageYOffset;")
        
        if current_scroll_position <= 0:
            break

def sanitize_filename(name):
    """Sanitize the name to make it safe for saving as a file."""
    name = name.replace(" ", "_")
    # Keep only alphanumeric characters, dots, and underscores (no spaces)
    return "".join(c for c in name if c.isalnum() or c in ('.', '_')).rstrip()

def extract_images_from_href(profile_url, name):
    """Extract images from the href (celebrity's profile page) and return their file paths."""
    images = []
    driver.get(profile_url)
    
    # Scrape main profile image from #profimg
    try:
        profimg = driver.find_element(By.ID, 'profimg')
        main_img_tag = profimg.find_element(By.TAG_NAME, 'a')
        main_img_url = urljoin('https://www.babepedia.com', main_img_tag.get_attribute('href'))
        main_img_name = sanitize_filename(unquote(os.path.basename(main_img_url)))
        img_filepath = download_image(main_img_url, main_img_name)
        if img_filepath:
            images.append([img_filepath, name])
    except Exception as e:
        print(f"Error scraping main profile image: {e}")

    # Scrape additional images from #profselect
    try:
        profselect = driver.find_element(By.ID, 'profselect')
        prof_imgs = profselect.find_elements(By.CLASS_NAME, 'prof')
        for img_div in prof_imgs:
            img_tag = img_div.find_element(By.TAG_NAME, 'a')
            img_url = urljoin('https://www.babepedia.com', img_tag.get_attribute('href'))
            img_name = sanitize_filename(unquote(os.path.basename(img_url)))
            img_filepath = download_image(img_url, img_name)
            if img_filepath:
                images.append([img_filepath, name])
    except Exception as e:
        print(f"Error scraping additional images: {e}")

    # Scrape user-uploaded images from .gallery.useruploads
    try:
        user_gallery = driver.find_element(By.CLASS_NAME, 'gallery.useruploads')
        user_imgs = user_gallery.find_elements(By.CLASS_NAME, 'thumbnail')
        for thumb in user_imgs:
            img_tag = thumb.find_element(By.TAG_NAME, 'a')
            img_url = urljoin('https://www.babepedia.com', img_tag.get_attribute('href'))
            img_name = sanitize_filename(unquote(os.path.basename(img_url)))
            img_filepath = download_image(img_url, img_name)
            if img_filepath:
                images.append([img_filepath, name])
    except Exception as e:
        print(f"Error scraping user-uploaded images: {e}")

    return images

def download_image(img_url, img_name):
    """Download an image and save it to the images_folder, ensuring the filename is unique, and log the process."""
    img_filepath = os.path.join(images_folder, img_name)
    
    # Check if the file already exists and append a number to make the name unique
    base_name, ext = os.path.splitext(img_name)
    counter = 1
    while os.path.exists(img_filepath):
        img_filepath = os.path.join(images_folder, f"{base_name}_{counter}{ext}")
        counter += 1
    
    response = requests.get(img_url, headers=headers)
    
    if response.status_code == 200:
        with open(img_filepath, 'wb') as img_file:
            img_file.write(response.content)
        # Log the successful download
        print(f"Successfully downloaded: {img_url} -> {img_filepath}")
        return img_filepath
    else:
        # Log the failed download
        print(f"Failed to download: {img_url}, Status code: {response.status_code}")
        return None


def extract_social_links(profile_url):
    """Extract the social media links from the profile page."""
    social_links = {}
    try:
        # Open the profile page
        driver.get(profile_url)
        
        # Find the social icons div
        social_icons_div = driver.find_element(By.ID, 'socialicons')
        social_icons = social_icons_div.find_elements(By.TAG_NAME, 'a')
        
        # Extract the URLs from the social icons
        for icon in social_icons:
            platform = icon.get_attribute('class').split()[-1]  # Get the platform name (e.g., instagram, tiktok)
            link = icon.get_attribute('href')
            social_links[platform] = link
    
    except Exception as e:
        print(f"Error extracting social links from {profile_url}: {e}")
    
    return social_links

def scrape_images(driver):
    """Scrape the images, names, and social media links from the href (profile page)."""
    scroll_direction_down = True  # Flag to track scrolling direction

    try:
        # Re-fetch the list of elements inside the loop to avoid stale elements
        elements = driver.find_elements(By.CLASS_NAME, 'thumbshot')

        for index, element in enumerate(elements):
            # Re-fetch the element by index to avoid stale references
            element = driver.find_elements(By.CLASS_NAME, 'thumbshot')[index]

            # Extract the name and href
            img_tag = element.find_element(By.TAG_NAME, 'img')
            name = img_tag.get_attribute('alt').replace("profile", "").replace("photo", "").strip()
            
            profile_tag = element.find_element(By.TAG_NAME, 'a')
            profile_href = profile_tag.get_attribute('href')
            profile_url = urljoin('https://www.babepedia.com', profile_href)

            # Extract images from the href
            image_data_from_profile = extract_images_from_href(profile_url, name)
            
            # Extract social media links from the profile page
            social_links = extract_social_links(profile_url)

            # Add the scraped data to the list, ensuring we append images from profile pages
            image_data = []
            for img_info in image_data_from_profile:
                image_data.append([img_info[0], name, social_links])

            # Log after each celebrity's images are downloaded
            print(f"Finished downloading images for {name}")
            save_data_to_csv(image_data, 'app/db/images/csv/onlyfans_data.csv')

            # After processing the profile, go back to the original page
            driver.back()

            # Alternate scrolling based on the flag
            if scroll_direction_down:
                print(f"Scrolling down after {name}")
                scroll_to_bottom(driver, scroll_pause_time=0.1, scroll_increment=1500)
                scroll_direction_down = False  # Next time scroll up
            else:
                print(f"Scrolling up after {name}")
                scroll_to_top(driver, scroll_pause_time=0.1, scroll_increment=1500)
                scroll_direction_down = True  # Next time scroll down

    except Exception as e:
        print(f"Error during image scraping: {e}")

def save_data_to_csv(data, csv_path):
    """Save the image data to a CSV file."""
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for row in data:
            # Flatten the social links dictionary into a comma-separated string
            social_links_str = ", ".join([f"{platform}*{link}" for platform, link in row[2].items()])
            writer.writerow([row[0], row[1], social_links_str])
    print(f"Data saved to {csv_path}")

def scrape_onlyfans_pages(num_pages):
    """Scrape images from the specified number of pages."""
    try:
        for page_num in range(1, num_pages + 1):
            url = f'https://www.babepedia.com/onlyfanstop100?page={page_num}'
            print(f"Scraping page: {url}")
            
            driver.get(url)
            
            scroll_to_bottom(driver, scroll_pause_time=0.1, scroll_increment=1500)
            scrape_images(driver)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(3)
        driver.quit()

# Start scraping
scrape_onlyfans_pages(1)
