import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

# Base URL of the site
base_url = "https://www.porn-star.com"

# Folder path
top100_folder = "app/db/images/images_top100"  

# Create folders if they don't exist
os.makedirs(top100_folder, exist_ok=True)

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

# Method 1: Scrape the top 100 images from the main page and save them to the specified folder
def scrape_top100_images():
    # URL of the page you want to scrape
    main_url = urljoin(base_url, "/top100.html")
    
    # Make a request to get the HTML content of the page
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # List to store the image file paths and names for CSV
    image_data = []

    # Find all div elements with the class "top100"
    top100_elements = soup.find_all('div', class_='top100')

    # Loop through each element and extract the <img src> and <a title>
    for element in top100_elements:
        # Extract the <img> tag and get the image URL
        img_tag = element.find('img')
        if img_tag:
            img_src = img_tag['src']
            img_name = os.path.basename(img_src)
            img_url = urljoin(base_url, img_src)
            img_filepath = os.path.join(top100_folder, img_name)

            # Extract the <a> tag and get the title (name)
            a_tag = element.find('a', title=True)
            if a_tag:
                name = a_tag['title']
                print(f"Downloading image for {name}: {img_url}")

                # Download the image
                try:
                    img_data = requests.get(img_url).content
                    with open(img_filepath, 'wb') as img_file:
                        img_file.write(img_data)
                    print(f"Saved: {img_filepath}")

                    # Add the file path and name to the list for CSV
                    image_data.append([img_filepath, name])
                except Exception as e:
                    print(f"Error downloading image for {name}: {e}")

    # Write the image data to a CSV file
    csv_filepath = 'app/db/images/csv/top100_image_data.csv'
    with open(csv_filepath, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(image_data)  # Write image data rows

    print(f"Top 100 images have been downloaded and saved in {csv_filepath}.")

# Method 2: Scrape image URLs from individual pages and save images
def scrape_individual_page_images():
    # URL of the page you want to scrape
    main_url = urljoin(base_url, "/top100.html")
    
    # Make a request to get the HTML content of the page
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
                
                # Create a folder inside 'images_celebrity' with the person's name
                folder_name = os.path.join(top100_folder, name.replace(" ", "_"))
                
                print(f"Scraping images for {name} from {href_url}...")

                # Scrape the images from the href page and save them to the folder
                try:
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
                except Exception as e:
                    print(f"Error scraping images for {name}: {e}")

    print("All individual images have been downloaded.")

# Run both methods
scrape_top100_images()
# scrape_individual_page_images()
