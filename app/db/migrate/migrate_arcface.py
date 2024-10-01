import psycopg2
import torch
from torchvision import transforms
from PIL import Image
import numpy as np
import pandas as pd
import insightface
from insightface.app import FaceAnalysis

# Set up the device for GPU usage if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Database connection setup
conn = psycopg2.connect(
    host="127.0.0.1",
    port="5432",
    database="celebrity",
    user="root",  # Ensure this is the correct username
    password="rootpassword"  # Ensure this is the correct password
)
cursor = conn.cursor()

# Drop the tables if they exist
cursor.execute("""
    DROP TABLE IF EXISTS vectorized_onlyfans_arcface;
    DROP TABLE IF EXISTS onlyfans_models_arcface;
""")
conn.commit()

# Enable the pgvector extension
cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
conn.commit()

# Create the 'onlyfans_models_arcface' table
cursor.execute("""
    CREATE TABLE onlyfans_models_arcface (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE,  -- Unique model name
        www TEXT,
        instagram TEXT,
        onlyfans TEXT,
        onlyfansfree TEXT,
        mym TEXT,
        tiktok TEXT,
        x TEXT,  -- For Twitter/X
        facebook TEXT,
        twitch TEXT,
        youtube TEXT,
        imdb TEXT,
        fansly TEXT,
        other TEXT  -- For any additional social media or links
    );
""")
conn.commit()

# Create the 'vectorized_onlyfans_arcface' table with a foreign key to 'onlyfans_models_arcface'
cursor.execute("""
    CREATE TABLE vectorized_onlyfans_arcface (
        id SERIAL PRIMARY KEY,
        name TEXT,
        img_path TEXT,
        feature_vector VECTOR(512),  -- The VECTOR(512) type is used for ArcFace embeddings
        model_id INTEGER REFERENCES onlyfans_models_arcface(id) ON DELETE CASCADE
    );
""")
conn.commit()

# Load the ArcFace model
app = FaceAnalysis(allowed_modules=['detection', 'recognition'])
app.prepare(ctx_id=0 if torch.cuda.is_available() else -1)

# Function to extract the feature vector from the ArcFace model
def extract_features_arcface(img_path):
    img = Image.open(img_path).convert('RGB')
    img_np = np.array(img)

    faces = app.get(img_np)

    if len(faces) == 0:
        raise ValueError("No face detected in the image.")

    # Assuming the first detected face is the one we want to use
    face = faces[0]
    features = face.embedding  # ArcFace embedding

    return features

# Function to extract social links from a string like "www*https://linkgenie.net/cristyren, instagram*https://instagram.com/cristyren"
def parse_social_links(social_links_str):
    # Initialize the social links dictionary
    social_links = {
        "www": None,
        "instagram": None,
        "onlyfans": None,
        "onlyfansfree": None,
        "mym": None,
        "tiktok": None,
        "x": None,
        "facebook": None,
        "twitch": None,
        "youtube": None,
        "imdb": None,
        "fansly": None,
        "other": None
    }

    # Check if social_links_str is valid and a string
    if isinstance(social_links_str, str):
        # Split the string and assign values
        for link in social_links_str.split(", "):
            if "*" in link:
                platform, url = link.split("*")
                if platform in social_links:
                    social_links[platform] = url
                else:
                    # If the platform is not recognized, add it to 'other'
                    social_links["other"] = (social_links["other"] or "") + f"{platform}*{url}, "
    
        # Remove trailing comma from 'other' if it exists
        if social_links["other"]:
            social_links["other"] = social_links["other"].rstrip(", ")

    return social_links

# Load the CSV file with image paths, names, and social media links
dataset = pd.read_csv('app/db/images/csv/onlyfans_data.csv', header=None, names=['Image File Path', 'Name', 'Social Links'])

# Insert data into the database
for index, row in dataset.iterrows():
    try:
        img_path = row['Image File Path']
        img_path = "app/db/images/" + img_path
        name = row['Name']
        social_links_str = row['Social Links']

        # Parse the social links into a dictionary
        social_links = parse_social_links(social_links_str)

        # Check if the model already exists
        cursor.execute("""
            SELECT id FROM onlyfans_models_arcface WHERE name = %s;
        """, (name,))
        result = cursor.fetchone()

        if result is None:
            # If the model doesn't exist, insert the model data
            cursor.execute("""
                INSERT INTO onlyfans_models_arcface (name, www, instagram, onlyfans, onlyfansfree, mym, tiktok, x, facebook, twitch, youtube, imdb, fansly, other)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (name, social_links['www'], social_links['instagram'], social_links['onlyfans'], 
                  social_links['onlyfansfree'], social_links['mym'], social_links['tiktok'], 
                  social_links['x'], social_links['facebook'], social_links['twitch'],
                  social_links['youtube'], social_links['imdb'], social_links['fansly'], social_links['other']))
            model_id = cursor.fetchone()[0]  # Get the new model ID
        else:
            # If the model exists, use the existing model ID
            model_id = result[0]

        # Extract features from the image using ArcFace
        features = extract_features_arcface(img_path)

        # Ensure features have the correct shape (512,)
        assert features.shape == (512,), f"Expected feature vector of size 512, but got {features.shape}"

        # Convert feature vector to a list for SQL
        feature_vector = features.tolist()

        # Insert the vectorized image and link it to the model
        cursor.execute("""
            INSERT INTO vectorized_onlyfans_arcface (name, img_path, feature_vector, model_id)
            VALUES (%s, %s, %s, %s);
        """, (name, img_path, feature_vector, model_id))

        # Commit after every successful insertion
        conn.commit()
        print(f"Successfully inserted {img_path}")

    except Exception as e:
        # Log the error and skip to the next row
        print(f"Error processing {img_path}: {e}")

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data and feature vectors have been stored in the database.")
