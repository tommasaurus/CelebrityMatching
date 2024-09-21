import psycopg2
import torch
from torchvision import models, transforms
from PIL import Image
import numpy as np
import pandas as pd
from torchvision.models.vision_transformer import ViT_B_16_Weights

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
    DROP TABLE IF EXISTS vectorized_onlyfans;
    DROP TABLE IF EXISTS onlyfans_models;
""")
conn.commit()

# Enable the pgvector extension
cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
conn.commit()

# Create the 'onlyfans_models' table
cursor.execute("""
    CREATE TABLE onlyfans_models (
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

# Create the 'vectorized_onlyfans' table with a foreign key to 'onlyfans_models'
cursor.execute("""
    CREATE TABLE vectorized_onlyfans (
        id SERIAL PRIMARY KEY,
        name TEXT,
        img_path TEXT,
        feature_vector VECTOR(1000),  -- pgvector type for storing feature vectors
        model_id INTEGER REFERENCES onlyfans_models(id) ON DELETE CASCADE  -- Foreign key reference
    );
""")
conn.commit()

# Load the pretrained Vision Transformer model and move to device
vit_b_16 = models.vit_b_16(weights=ViT_B_16_Weights.DEFAULT).to(device)
vit_b_16.eval()

# Image preprocessing pipeline for ViT (resize to 224x224 as ViT expects patches)
preprocess = transforms.Compose([
    transforms.Resize(224),  # Resize image for ViT
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Function to extract the feature vector from the model
def extract_features(img_path, model):
    img = Image.open(img_path).convert('RGB')
    img_tensor = preprocess(img).unsqueeze(0).to(device)
    
    with torch.no_grad():
        # Extract features using the forward method
        outputs = model(img_tensor)  # Shape: (batch_size, 1000)
        features = outputs.squeeze()  # Shape: (1000,)

    # Convert to numpy array and return
    return features.cpu().numpy()

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
dataset = pd.read_csv('app/db/images/csv/test.csv', header=None, names=['Image File Path', 'Name', 'Social Links'])

# Insert data into the database
for index, row in dataset.iterrows():
    try:
        img_path = row['Image File Path']
        name = row['Name']
        social_links_str = row['Social Links']

        # Parse the social links into a dictionary
        social_links = parse_social_links(social_links_str)

        # Check if the model already exists
        cursor.execute("""
            SELECT id FROM onlyfans_models WHERE name = %s;
        """, (name,))
        result = cursor.fetchone()

        if result is None:
            # If the model doesn't exist, insert the model data
            cursor.execute("""
                INSERT INTO onlyfans_models (name, www, instagram, onlyfans, onlyfansfree, mym, tiktok, x, facebook, twitch, youtube, imdb, fansly, other)
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

        # Extract features from the image
        features = extract_features(img_path, vit_b_16)

        # Ensure features have the correct shape (1000,)
        assert features.shape == (1000,), f"Expected feature vector of size 1000, but got {features.shape}"

        # Convert feature vector to a list for SQL
        feature_vector = features.tolist()

        # Insert the vectorized image and link it to the model
        cursor.execute("""
            INSERT INTO vectorized_onlyfans (name, img_path, feature_vector, model_id)
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
