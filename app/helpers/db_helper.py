# helpers/db_helper.py

import psycopg2
from psycopg2 import pool 
from dotenv import load_dotenv
import os

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

def get_social_links_by_model_name(name):
    """
    Fetch social links from the database for a given model name.
    """
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT www, instagram, onlyfans, onlyfansfree, mym, tiktok, x, facebook, twitch, youtube, imdb, fansly, other
                FROM onlyfans_models_arcface
                WHERE name = %s;
            """, (name,))
            
            result = cursor.fetchone()
            
            if result:
                # Construct a dictionary with the retrieved data
                social_links = {
                    "www": result[0],
                    "instagram": result[1],
                    "onlyfans": result[2],
                    "onlyfansfree": result[3],
                    "mym": result[4],
                    "tiktok": result[5],
                    "x": result[6],
                    "facebook": result[7],
                    "twitch": result[8],
                    "youtube": result[9],
                    "imdb": result[10],
                    "fansly": result[11],
                    "other": result[12]
                }
                return social_links
            else:
                return None
    except Exception as e:
        raise Exception(f"Error fetching social links from database: {e}")
    finally:
        connection_pool.putconn(conn)

def get_social_links_by_model_id(model_id):
    """
    Fetch social links from the database for a given model_id.
    """

    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cursor:
            # Query the database to get the social media links for the given model_id
            cursor.execute("""
                SELECT name, www, instagram, onlyfans, onlyfansfree, mym, tiktok, x, facebook, twitch, youtube, imdb, fansly, other
                FROM onlyfans_models_arcface
                WHERE id = %s;
            """, (model_id,))
            
            result = cursor.fetchone()
            
            if result:
                # Construct a dictionary with the retrieved data
                social_links = {
                    "name": result[0],
                    "www": result[1],
                    "instagram": result[2],
                    "onlyfans": result[3],
                    "onlyfansfree": result[4],
                    "mym": result[5],
                    "tiktok": result[6],
                    "x": result[7],
                    "facebook": result[8],
                    "twitch": result[9],
                    "youtube": result[10],
                    "imdb": result[11],
                    "fansly": result[12],
                    "other": result[13]
                }
                return social_links
            else:
                return None
    except Exception as e:
        raise Exception(f"Error fetching social links from database: {e}")

    finally:
        connection_pool.putconn(conn)

