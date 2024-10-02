from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import RedirectResponse

from app.api.image_routes import router as image_router

import os
from pathlib import Path
from urllib.parse import quote

from app.services.arcface import find_top_5_similar_from_db  # Updated import
from app.helpers.db_helper import get_social_links_by_model_id, get_social_links_by_model_name

from botocore.exceptions import NoCredentialsError

from app.services.s3_client import s3_client, S3_BUCKET


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image_router)

async def get_image(image_key: str):
    """
    Endpoint to retrieve an image from S3 using a pre-signed URL and redirect.
    """
    try:
        # Generate a pre-signed URL to access the image in S3
        image_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': image_key},
            ExpiresIn=900  # URL expires in 15 minutes
        )
        # Redirect the client to the pre-signed URL
        return RedirectResponse(url=image_url)
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving image: {str(e)}")


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    """
    Endpoint to upload an image, process it using ArcFace, and return the top matches.
    """
    try:
        contents = await file.read()

        # Define a temporary path for saving the file
        temp_directory = Path("app/tmp")
        temp_directory.mkdir(parents=True, exist_ok=True)

        temp_path = temp_directory / file.filename

        # Save the file temporarily
        with open(temp_path, "wb") as temp_file:
            temp_file.write(contents)

        # Run the ArcFace model to find the top 5 similar images
        onlyfans_results = find_top_5_similar_from_db(str(temp_path), 'vectorized_onlyfans_arcface')

        # Remove the temporary file after processing
        os.remove(temp_path)

        # Prepare the results
        matches = []
        for match in onlyfans_results:
            image_path, name, similarity, model_id = match
            # Convert similarity to a native Python float
            similarity = float(similarity)
            image_key = f"{quote(image_path)}"            
            
            try:
                # Generate a pre-signed URL for each matched image
                image_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': S3_BUCKET, 'Key': image_key},
                    ExpiresIn=900
                )
            except Exception as e:
                image_url = None

            # Fetch social links
            social_links = get_social_links_by_model_id(model_id)
            if social_links is None:
                social_links = {}            

            matches.append({
                "image_url": image_url,
                "name": name,
                "similarity": similarity,
                "model_id": model_id,
                "social_links": social_links
            })

        # Return the results
        return {"matches": matches}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")



@app.get("/get-social-links/{model_id}")
async def get_social_links(model_id: int):
    """
    Endpoint to retrieve social links for a given model ID.
    """
    try:
        social_links = get_social_links_by_model_id(model_id)
        if social_links:
            return {"model_id": model_id, "social_links": social_links}
        else:
            raise HTTPException(status_code=404, detail="Model not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving social links: {str(e)}")

@app.get("/get-social-links-by-name/{name}")
async def get_social_links_by_name(name: str):
    try:
        social_links = get_social_links_by_model_name(name)
        if social_links:
            return {"social_links": social_links}
        else:
            return {"social_links": {}}
    except Exception as e:
        print(f"Error fetching social links: {e}")
        return {"social_links": {}}
