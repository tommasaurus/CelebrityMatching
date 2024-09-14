import requests
from bs4 import BeautifulSoup
import os
import csv

# URL of the page you want to scrape
url = 'https://www.babepedia.com/pornstartop100'

# Make a request to get the HTML content of the page
response = requests.get(url)

html_content = response.text

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Create a folder to store the downloaded images
if not os.path.exists('downloaded_images'):
    os.makedirs('downloaded_images')

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
        img_url = f"https://www.porn-star.com{img_src}"  # Form the full URL
        img_name = img_src.split('/')[-1]  # Get the image filename
        img_filepath = os.path.join('downloaded_images', img_name)  # Local filepath

        # Extract the <a> tag and get the title (name)
        a_tag = element.find('a', title=True)
        if a_tag:
            name = a_tag['title']
            print(f"Downloading image for {name}: {img_url}")

            # Download the image
            img_data = requests.get(img_url).content
            with open(img_filepath, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Saved: {img_filepath}")

            # Add the file path and name to the list for CSV
            image_data.append([img_filepath, name])

# Write the image data to a CSV file
csv_filepath = 'image_data.csv'
with open(csv_filepath, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Image File Path', 'Name'])  # Write header
    csv_writer.writerows(image_data)  # Write image data rows

print(f"All images have been downloaded and saved in {csv_filepath}.")
