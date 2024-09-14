import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image, ImageOps
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from torchvision.models.vision_transformer import ViT_B_16_Weights

# Set up the device for GPU usage if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the pretrained Vision Transformer model and move to device
vit_b_16 = models.vit_b_16(weights=ViT_B_16_Weights.DEFAULT).to(device)  # Use the correct weights argument
vit_b_16.eval()

# Image preprocessing pipeline for ViT (resize to 224x224 as ViT expects patches)
preprocess = transforms.Compose([
    transforms.Resize(224),  # Resize image for ViT
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Batch feature extraction
def extract_features_batch(image_paths, model, batch_size=32):
    # Store all features
    all_features = []

    # Process images in batches
    for i in range(0, len(image_paths), batch_size):
        batch_paths = image_paths[i:i + batch_size]
        batch_images = []

        # Load and preprocess each image in the batch
        for img_path in batch_paths:
            img = Image.open(img_path).convert('RGB')
            img_tensor = preprocess(img).unsqueeze(0)  # Preprocess and add batch dimension
            batch_images.append(img_tensor)

        # Stack all images into a single tensor
        batch_tensor = torch.cat(batch_images).to(device)  # Combine tensors and move to GPU if available

        with torch.no_grad():
            # Forward pass through the model
            batch_features = model(batch_tensor)
            batch_features = batch_features.squeeze()

            # Flatten features if necessary
            if batch_features.ndim > 2:
                batch_features = batch_features.view(batch_features.size(0), -1)
        
        # Move to CPU and convert to numpy
        batch_features = batch_features.cpu().numpy()

        # Append features to the list
        all_features.extend(batch_features)

    return np.array(all_features)

# Load the CSV file with image paths and names
dataset = pd.read_csv('image_data.csv', header=None, names=['Image File Path', 'Name'])

# Extract features for each image in the dataset using batch processing
database_features = extract_features_batch([row['Image File Path'] for _, row in dataset.iterrows()], vit_b_16)
database_names = [row['Name'] for _, row in dataset.iterrows()]

# Function to find the top 5 most similar images in the dataset
def find_top_5_similar_batch(input_img_paths, batch_size=32):
    # Extract features for the input images in batch
    input_features = extract_features_batch(input_img_paths, vit_b_16, batch_size=batch_size)
    
    # Compute cosine similarity for the entire batch
    similarities = cosine_similarity(input_features, database_features)
    
    # Find the indices of the top 5 most similar images for each input image
    top_5_indices_batch = [np.argsort(similarity)[-5:][::-1] for similarity in similarities]
    
    # Retrieve the top 5 most similar images and their names for each input
    all_top_5_matches = []
    for top_5_indices in top_5_indices_batch:
        top_5_matches = [(dataset.iloc[i]['Image File Path'], database_names[i]) for i in top_5_indices]
        all_top_5_matches.append(top_5_matches)
    
    return all_top_5_matches

def pad_and_show_images_side_by_side(image_paths, model, save_path):
    input_images = [Image.open(img_path).convert('RGB') for img_path in image_paths]
    output_images = []

    # Find the most similar output images for each input image in batch
    most_similar_images_batch = find_top_5_similar_batch(image_paths)
    
    for matches in most_similar_images_batch:
        # Take the most similar image (first one in the sorted list)
        most_similar_img_path, _ = matches[0]
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
input_image_paths = ['images/abella.jpg', 'images/abella.webp', 'images/margot.webp', 'images/abella2.jpg', 'images/lana.jpg', 'images/kenzie.jpg', 'images/rae.jpg']
pad_and_show_images_side_by_side(input_image_paths, vit_b_16, 'comparison_multiple_pairs.jpg')

print("Image comparison saved as 'comparison_multiple_pairs.jpg'")
