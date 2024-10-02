# app/api/image_routes.py
from fastapi import APIRouter
from pathlib import Path
import random
import csv
from botocore.exceptions import NoCredentialsError
from app.services.s3_client import s3_client, S3_BUCKET

router = APIRouter()

# Path to your CSV file
CSV_PATH = Path("app/db/images/csv/onlyfans_data.csv")

@router.get("/random-images")
async def get_random_images(count: int = 5):
    """
    Fetch random images from the CSV and include pre-signed URLs.
    """
    csv_path = CSV_PATH
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f, fieldnames=["image_path", "name", "social_links"])
        images = list(reader)

    # Randomly sample images from the CSV
    random_images = random.sample(images, min(count, len(images)))

    # Create image URLs based on the file path from the CSV
    image_urls = []
    for image in random_images:
        image_filename = Path(image['image_path']).name
        image_key = f"images_onlyfans/{image_filename}"
        try:
            # Generate a pre-signed URL
            image_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_BUCKET, 'Key': image_key},
                ExpiresIn=900
            )
            image_urls.append({
                "image_url": image_url,
                "name": image["name"]
            })
        except NoCredentialsError:
            continue
        except Exception as e:
            continue

    return {"images": image_urls}
