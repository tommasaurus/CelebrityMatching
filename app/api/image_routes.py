# app/api/image_routes.py
from fastapi import APIRouter
from pathlib import Path
import random
import csv

router = APIRouter()

# Path to your CSV file
CSV_PATH = Path("app/db/images/csv/onlyfans_data.csv")

# app/api/image_routes.py
@router.get("/random-images")
async def get_random_images(count: int = 5):
    """
    Fetch random images from the `images_onlyfans` folder, with file paths from the CSV.
    """
    # Ensure you're using the correct CSV path
    csv_path = Path("app/db/images/csv/onlyfans_data.csv")
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f, fieldnames=["image_path", "name", "social_links"])
        images = list(reader)

    # Randomly sample images from the CSV
    random_images = random.sample(images, min(count, len(images)))

    # Create image URLs based on the file path from the CSV
    image_urls = [{
        "image_url": f"{image['image_path']}",  # Adjust the URL path to match your FastAPI static route
        "name": image["name"]
    } for image in random_images]

    return {"images": image_urls}
