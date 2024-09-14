import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image, ImageOps
import pandas as pd
import numpy as np

# Load the pretrained Vision Transformer model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
vit_b_16 = models.vit_b_16(weights=models.ViT_B_16_Weights.DEFAULT).to(device)   # Use the correct weights argument
vit_b_16.eval()

# Image preprocessing pipeline for ViT (resize to 224x224 as ViT expects patches)
preprocess = transforms.Compose([
    transforms.Resize(224),  # Resize image for ViT
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Function to extract feature vectors from a batch of images using ViT
def extract_features_batch(image_paths, model, batch_size=32):
    features_list = []
    for i in range(0, len(image_paths), batch_size):
        batch_paths = image_paths[i:i + batch_size]
        images = [preprocess(Image.open(img_path).convert('RGB')) for img_path in batch_paths]
        batch_tensor = torch.stack(images)
        
        with torch.no_grad():
            batch_features = model(batch_tensor)
            batch_features = batch_features.view(batch_features.size(0), -1)
            features_list.append(batch_features.numpy())

    return np.vstack(features_list)

# Load the CSV file with image paths and names
dataset = pd.read_csv('image_data.csv', header=None, names=['Image File Path', 'Name'])

# Extract features for the entire dataset in one go (batch processing)
database_features = extract_features_batch(dataset['Image File Path'].tolist(), vit_b_16)
database_names = dataset['Name'].tolist()
database_paths = dataset['Image File Path'].tolist()

# Function to compute cosine similarity using NumPy
def cosine_similarity_numpy(features, database_features):
    features = features / np.linalg.norm(features, axis=1, keepdims=True)
    database_features = database_features / np.linalg.norm(database_features, axis=1, keepdims=True)
    return np.dot(features, database_features.T)

# Function to find the top 5 most similar images in the dataset
def find_top_5_similar(input_img_path):
    # Extract features for the input image
    input_features = extract_features_batch([input_img_path], vit_b_16)

    # Compute cosine similarity between input image and database images using NumPy
    similarities = cosine_similarity_numpy(input_features, database_features)[0]

    # Find the indices of the top 5 most similar images
    top_5_indices = np.argsort(similarities)[-5:][::-1]

    # Retrieve the top 5 most similar images and their names
    top_5_matches = [(database_paths[i], database_names[i], similarities[i]) for i in top_5_indices]
    
    print("Top 5 similar images:")
    for img_path, name, similarity in top_5_matches:
        print(f"Image: {img_path}, Name: {name}, Similarity: {similarity}")
    
    return top_5_matches

# Function to show images side by side
def pad_and_show_images_side_by_side(image_paths, model, save_path):
    input_images = [Image.open(img_path).convert('RGB') for img_path in image_paths]
    output_images = []
    
    # Find the most similar output images for each input image
    for img_path in image_paths:
        most_similar_img_path, _, _ = find_top_5_similar(img_path)[0]  # Get the most similar image
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
