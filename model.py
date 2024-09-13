import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the pretrained ResNet50 model
resnet50 = models.resnet50(pretrained=True)

# Remove the final classification layer to get feature vectors
model = nn.Sequential(*list(resnet50.children())[:-1])
model.eval()  # Set model to evaluation mode

# Image preprocessing pipeline (resize, center crop, normalize)
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Function to extract feature vector from an image
def extract_features(img_path, model):
    img = Image.open(img_path).convert('RGB')  # Open image
    img_tensor = preprocess(img).unsqueeze(0)  # Preprocess and add batch dimension
    with torch.no_grad():  # No need to calculate gradients
        features = model(img_tensor).squeeze()  # Extract features
    return features.numpy()

# Load the CSV file with image paths and names
dataset = pd.read_csv('image_data.csv', header=None, names=['Image File Path', 'Name'])

# Extract features for each image in the dataset
database = []
for index, row in dataset.iterrows():
    img_path = row['Image File Path']
    name = row['Name']
    features = extract_features(img_path, model)
    database.append((features, img_path, name))

# Save the features to avoid recalculating them
database_features = np.array([item[0] for item in database])
database_names = [item[2] for item in database]

# Function to find the top 5 most similar images in the dataset
def find_top_5_similar(input_img_path):
    # Extract features for the input image
    input_features = extract_features(input_img_path, model)
    
    # Compute cosine similarity between input image and database images
    similarities = cosine_similarity([input_features], database_features)[0]
    
    # Find the indices of the top 5 most similar images
    top_5_indices = np.argsort(similarities)[-5:][::-1]
    
    # Retrieve the top 5 most similar images and their names
    top_5_matches = [(dataset.iloc[i]['Image File Path'], database_names[i], similarities[i]) for i in top_5_indices]
    
    print("Top 5 similar images:")
    for img_path, name, similarity in top_5_matches:
        print(f"Image: {img_path}, Name: {name}, Similarity: {similarity}")
    
    return top_5_matches

# Example usage: Input image to match
input_image_path = 'abella.jpg'  # Path to the test image you want to input
top_5_matches = find_top_5_similar(input_image_path)

print("BREAK")

input_image_path = 'abella2.jpg'  # Path to the test image you want to input
top_5_matches = find_top_5_similar(input_image_path)