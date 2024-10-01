import os
import torch
import numpy as np
import psycopg2
from psycopg2 import pool
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import psycopg2.extras
from pgvector.psycopg2 import register_vector
from insightface.app import FaceAnalysis
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='./app/.env')

# # Database connection setup (adjust as per your environment)
# connection_pool = pool.SimpleConnectionPool(
#     minconn=1,
#     maxconn=10,
#     host="localhost",
#     port="5432",
#     database="celebrity",
#     user="root",
#     password="rootpassword"
# )

db_host = os.getenv("RDS_HOST")
db_user = os.getenv("RDS_USER")
db_password = os.getenv("RDS_PASSWORD")

connection_pool = pool.SimpleConnectionPool(
    minconn=1, 
    maxconn=10,  # You can adjust the max connections as per your application load
    host=db_host,
    port="5432",
    database="celebritymatching_db",
    user=db_user,
    password=db_password
)

# Set up the device for GPU usage if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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

# Function to load feature vectors and metadata from a specified database table
def load_database_features(table_name):
    conn = connection_pool.getconn()
    register_vector(conn)  # Register pgvector extension

    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT img_path, name, feature_vector, model_id FROM {table_name};")
            rows = cursor.fetchall()

            database_paths = []
            database_names = []
            database_features = []
            database_model_id = []

            for row in rows:
                img_path, name, feature_vector, model_id = row
                database_paths.append(img_path)
                database_names.append(name)
                database_features.append(np.array(feature_vector))
                database_model_id.append(model_id)

            database_features = np.array(database_features)
            return database_features, database_names, database_paths, database_model_id

    except Exception as e:
        print(f"Error loading database features: {e}")
        return np.array([]), [], [], []

    finally:
        connection_pool.putconn(conn)

# Function to find the top 5 most similar unique models in the specified database table
def find_top_5_similar_from_db(input_img_path, table_name):
    # Load the feature vectors and metadata from the specified database table
    database_features, database_names, database_paths, database_model_id = load_database_features(table_name)

    if len(database_features) == 0:
        print(f"No features found in the database table: {table_name}")
        return []

    # Extract features for the input image
    input_features = extract_features_arcface(input_img_path).reshape(1, -1)

    # Compute cosine similarity between input image and database images
    similarities = cosine_similarity(input_features, database_features)[0]

    # Dictionary to hold the highest similarity for each unique model_id
    model_similarity = {}
    model_image_info = {}

    # Iterate over all similarities and update the model_similarity dictionary
    for i in range(len(similarities)):
        model_id = database_model_id[i]
        sim = similarities[i]
        if model_id not in model_similarity or sim > model_similarity[model_id]:
            model_similarity[model_id] = sim
            model_image_info[model_id] = (database_paths[i], database_names[i])

    # Create a list of models with their max similarities
    model_similarity_list = []
    for model_id, sim in model_similarity.items():
        img_path, name = model_image_info[model_id]
        model_similarity_list.append((img_path, name, sim, model_id))

    # Sort the models by similarity in descending order
    top_matches_sorted = sorted(model_similarity_list, key=lambda x: x[2], reverse=True)

    # Get the top 5 unique matches
    top_5_matches = top_matches_sorted[:5]

    print(f"Top 5 similar unique models from {table_name}:")
    for img_path, name, similarity, model_id in top_5_matches:
        print(f"Image: {img_path}, Name: {name}, Similarity: {similarity}, Model ID: {model_id}")

    return top_5_matches

if __name__ == "__main__":
    # Example usage
    input_image_path = 'app/services/images/kylie.jpg'
    find_top_5_similar_from_db(input_image_path, 'vectorized_onlyfans_arcface')
