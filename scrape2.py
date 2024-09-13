import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL of the site
base_url = "https://www.porn-star.com"

# Folder to store all images
main_folder = "downloaded_images"

# Create main folder if it doesn't exist
if not os.path.exists(main_folder):
    os.makedirs(main_folder)

# Function to download an image from a URL and save it to a specific folder
def download_image(img_url, folder_path, img_name):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Download the image
    img_data = requests.get(img_url).content
    img_path = os.path.join(folder_path, img_name)
    
    # Save the image to the folder
    with open(img_path, 'wb') as handler:
        handler.write(img_data)
    print(f"Downloaded: {img_path}")

# Function to scrape image URLs from the href page and save images
def scrape_and_save_images(href_url, folder_name):
    response = requests.get(href_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for the div containing the thumbnails
    thumbnails_div = soup.find('div', class_='thumbnails-pictures')
    if thumbnails_div:
        # Find all the <img> tags within that div
        img_tags = thumbnails_div.find_all('img')
        for img_tag in img_tags:
            img_src = img_tag['src']
            img_name = os.path.basename(img_src)
            img_full_url = urljoin(href_url, img_src)
            
            # Save the image to the corresponding folder
            download_image(img_full_url, folder_name, img_name)

# Step 1: Scrape the main page to get the image, title, and href
main_url = "https://www.porn-star.com/top100.html"
response = requests.get(main_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all divs with the class "top100"
top100_elements = soup.find_all('div', class_='top100')

# Loop through each element and extract the <img src>, <a title>, and href
for element in top100_elements:
    # Extract the <img> tag and get the image URL
    img_tag = element.find('img')
    if img_tag:
        img_src = img_tag['src']
        img_name = os.path.basename(img_src)
        img_url = urljoin(base_url, img_src)

        # Extract the <a> tag and get the title (name)
        a_tag = element.find('a', title=True)
        if a_tag:
            name = a_tag['title']
            href = a_tag['href']
            href_url = urljoin(base_url, href)
            
            # Create a folder inside 'downloaded_images' with the person's name
            folder_name = os.path.join(main_folder, name.replace(" ", "_"))
            
            print(f"Scraping images for {name} from {href_url}...")

            # Scrape the images from the href page and save them to the folder
            scrape_and_save_images(href_url, folder_name)
            
print("All images have been downloaded.")
