import os
from fastapi import FastAPI, File, UploadFile
from pathlib import Path
from app.services.vitdb import find_top_5_similar_from_db

app = FastAPI()

# Define the upload directory
UPLOAD_DIRECTORY = "app/services/uploads/"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # Save the uploaded file to the specified directory
    upload_path = Path(UPLOAD_DIRECTORY) / file.filename
    with open(upload_path, "wb") as buffer:
        buffer.write(await file.read())

    # Run the model to find the top 5 similar images in the 'celebrity_features' table
    celebrity_results = find_top_5_similar_from_db(str(upload_path), 'celebrity_features')

    # Run the model to find the top 5 similar images in the 'onlyfans_features' table
    onlyfans_results = find_top_5_similar_from_db(str(upload_path), 'onlyfans_features')

    # Return the results
    return {
        "celebrity_matches": [{"image_path": match[0], "name": match[1], "similarity": match[2]} for match in celebrity_results],
        "onlyfans_matches": [{"image_path": match[0], "name": match[1], "similarity": match[2]} for match in onlyfans_results],
    }
