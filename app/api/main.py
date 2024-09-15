import os
from fastapi import FastAPI, File, UploadFile
from pathlib import Path
from app.services.vitdb import find_top_5_similar_from_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi.responses import FileResponse
from urllib.parse import unquote, quote

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the upload directory
UPLOAD_DIRECTORY = "app/services/uploads/"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
IMAGE_DIR = os.path.join("app", "db", "images", "images_onlyfans")

@app.get("/images/{image_name}")
async def get_image(image_name: str):
    # Decode the URL-encoded image_name    
    image_path = os.path.join(IMAGE_DIR, image_name)
    print(f"Decoded path: {image_path}")    

    # Check if the image exists
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail=f"Image not found: {image_path}")
    
    # Return the image
    return FileResponse(image_path)


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # Save the uploaded file to the specified directory
    upload_path = Path(UPLOAD_DIRECTORY) / file.filename
    with open(upload_path, "wb") as buffer:
        buffer.write(await file.read())

    # Run the model to find the top 5 similar images in the 'onlyfans_features' table
    onlyfans_results = find_top_5_similar_from_db(str(upload_path), 'onlyfans_features')

    # Get the first match from the results
    top_match_image_path = onlyfans_results[0][0]  # This is the image path of the top match
    
    # Extract the image filename to use in the URL
    top_match_image_name = os.path.basename(top_match_image_path)
    top_match_image_name = quote(top_match_image_name)

    # Return the results
    return {
        "top_match_image_url": top_match_image_name,  # Include the URL of the top match image
        "onlyfans_matches": [{"image_path": match[0], "name": match[1], "similarity": match[2]} for match in onlyfans_results],
    }