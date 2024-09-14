import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image, ImageOps
import numpy as np
import psycopg2
from sklearn.metrics.pairwise import cosine_similarity
from torchvision.models.vision_transformer import ViT_B_16_Weights

# Database connection setup
conn = psycopg2.connect(
    host="127.0.0.1",  # Use 'localhost' or the IP address of the host machine
    port="5432",       # Default PostgreSQL port
    database="celebrity",
    user="root",       # Ensure this is the correct username
    password="rootpassword"  # Ensure this is the correct password
)
cursor = conn.cursor()

# Set up the device for GPU usage if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the pretrained Vision Transformer model and move to device
vit_b_16 = models.vit_b_16(weights=ViT_B_16_Weights.DEFAULT).to(device)
vit_b_16.eval()

# Image preprocessing pipeline for ViT (resize to 224x224 as ViT expects patches)
preprocess = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Function to extract feature vector from an image using ViT
def extract_features(img_path, model):
    img = Image.open(img_path).convert('RGB')
    img_tensor = preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad():
        features = model(img_tensor)
        features = features.squeeze()
        if features.ndim > 1:
            features = features.view(-1)
    return features.cpu().numpy()

# Function to load feature vectors and metadata from a specified database table
def load_database_features(table_name):
    cursor.execute(f"SELECT img_path, name, feature_vector FROM {table_name};")
    rows = cursor.fetchall()
    database_paths = []
    database_names = []
    database_features = []

    for row in rows:
        img_path, name, feature_vector_str = row
        database_paths.append(img_path)
        database_names.append(name)
        
        # Parse the feature vector string into a NumPy array
        feature_vector = np.fromstring(feature_vector_str.strip('[]'), sep=',')  # Convert string to float array
        database_features.append(feature_vector)

    return np.array(database_features), database_names, database_paths

# Function to find the top 5 most similar images in the specified database table
def find_top_5_similar_from_db(input_img_path, table_name):
    # Load the feature vectors and metadata from the specified database table
    database_features, database_names, database_paths = load_database_features(table_name)

    # Extract features for the input image
    input_features = extract_features(input_img_path, vit_b_16).reshape(1, -1)

    # Compute cosine similarity between input image and database images
    similarities = cosine_similarity(input_features, database_features)[0]

    # Find the indices of the top 5 most similar images
    top_5_indices = np.argsort(similarities)[-5:][::-1]

    # Retrieve the top 5 most similar images and their names
    top_5_matches = [(database_paths[i], database_names[i], similarities[i]) for i in top_5_indices]
    
    print(f"Top 5 similar images from {table_name}:")
    for img_path, name, similarity in top_5_matches:
        print(f"Image: {img_path}, Name: {name}, Similarity: {similarity}")
    
    return top_5_matches

# Function to show images side by side from a specified database table
def pad_and_show_images_side_by_side(image_paths, table_name, save_path):
    input_images = [Image.open(img_path).convert('RGB') for img_path in image_paths]
    output_images = []

    # Find the most similar output images for each input image from the specified table
    for img_path in image_paths:
        most_similar_img_path, _, _ = find_top_5_similar_from_db(img_path, table_name)[0]  # Get the most similar image
        output_images.append(Image.open(most_similar_img_path).convert('RGB'))

    # Get the maximum width and height of all the images (both input and output)
    max_width = max(max(img.size[0] for img in input_images), max(img.size[0] for img in output_images))
    max_height = max(max(img.size[1] for img in input_images), max(img.size[1] for img in output_images))

    # Pad all images to the same size while keeping their aspect ratios
    padded_input_images = [ImageOps.pad(img, (max_width, max_height), color=(128, 128, 128)) for img in input_images]
    padded_output_images = [ImageOps.pad(img, (max_width, max_height), color=(128, 128, 128)) for img in output_images]

    # Create a new image canvas with enough width to place each input/output pair side by side
    total_width = max_width * 2  # input + output side by side
    total_height = max_height * len(image_paths)  # Stack the pairs vertically

    new_img = Image.new('RGB', (total_width, total_height))

    # Paste input and output images side by side
    for i in range(len(image_paths)):
        new_img.paste(padded_input_images[i], (0, i * max_height))  # Paste input image
        new_img.paste(padded_output_images[i], (max_width, i * max_height))  # Paste corresponding output image

    # Save the new image for comparison
    new_img.save(save_path)
    new_img.show()  # Optionally, show the image for visual confirmation

# Example usage: An array of input images
input_image_paths = ['images/scarlett.webp', 'images/emma.jpg']

# Compare against the 'celebrity_features' table
pad_and_show_images_side_by_side(input_image_paths, 'celebrity_features', 'comparison_celebrity_pairs.jpg')
print("Image comparison against 'celebrity_features' saved as 'comparison_celebrity_pairs.jpg'")

# Compare against the 'onlyfans_features' table
pad_and_show_images_side_by_side(input_image_paths, 'onlyfans_features', 'comparison_onlyfans_pairs.jpg')
print("Image comparison against 'onlyfans_features' saved as 'comparison_onlyfans_pairs.jpg'")

# Close the database connection
cursor.close()
conn.close()
