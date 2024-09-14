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

# Drop the table if it exists
cursor.execute("""
    DROP TABLE IF EXISTS celebrity_features;
""")
conn.commit()

# Create the table with the correct feature vector size
cursor.execute("""
    CREATE TABLE celebrity_features (
        id SERIAL PRIMARY KEY,
        img_path TEXT,
        name TEXT,
        feature_vector VECTOR(1000)  -- Adjust this column type to match the output vector size
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

# Load the CSV file with image paths and names
dataset = pd.read_csv('image_data.csv', header=None, names=['Image File Path', 'Name'])

# Insert data into the database
for index, row in dataset.iterrows():
    img_path = row['Image File Path']
    name = row['Name']
    features = extract_features(img_path, vit_b_16)

    # Ensure features have the correct shape (1000,)
    assert features.shape == (1000,), f"Expected feature vector of size 1000, but got {features.shape}"

    # Convert feature vector to a list for SQL
    feature_vector = features.tolist()

    # SQL command to insert data into the table
    cursor.execute("""
        INSERT INTO celebrity_features (img_path, name, feature_vector)
        VALUES (%s, %s, %s)
    """, (img_path, name, feature_vector))

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Features have been stored in the database.")
