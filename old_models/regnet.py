import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image, ImageOps
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


regnet_y_32gf = models.regnet_y_32gf(pretrained=True)
model = nn.Sequential(*list(regnet_y_32gf.children())[:-1])
model.eval()


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

    if features.ndim > 1:
        features = features.view(-1)
            
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

# # Example usage: Input image to match
# input_image_path = 'images/abella.jpg'  # Path to the test image you want to input
# top_5_matches = find_top_5_similar(input_image_path)

# print("BREAK")

# input_image_path = 'images/abella2.jpg'  # Path to the test image you want to input
# top_5_matches = find_top_5_similar(input_image_path)

# print("BREAK")

# input_image_path = 'images/kylie.jpg'  # Path to the test image you want to input
# top_5_matches = find_top_5_similar(input_image_path)

# print("BREAK")

# input_image_path = 'images/margot.webp'  # Path to the test image you want to input
# top_5_matches = find_top_5_similar(input_image_path)
def find_most_similar(input_img_path):
    # Extract features for the input image
    input_features = extract_features(input_img_path, model)
    
    # Compute cosine similarity between input image and database images
    similarities = cosine_similarity([input_features], database_features)[0]
    
    # Find the index of the most similar image
    most_similar_index = np.argmax(similarities)
    
    # Return the most similar image path and name
    most_similar_img_path = dataset.iloc[most_similar_index]['Image File Path']
    most_similar_name = database_names[most_similar_index]
    
    return most_similar_img_path, most_similar_name

def pad_and_show_images_side_by_side(image_paths, model, save_path):
    input_images = [Image.open(img_path).convert('RGB') for img_path in image_paths]
    output_images = []
    
    # Find the most similar output images for each input image
    for img_path in image_paths:
        most_similar_img_path, _ = find_most_similar(img_path)
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
input_image_paths = ['images/abella.jpg', 'images/abella.webp', 'images/margot.webp', 'images/abella2.jpg']
pad_and_show_images_side_by_side(input_image_paths, model, 'comparison_multiple_pairs.jpg')

print("Image comparison saved as 'comparison_multiple_pairs.jpg'")