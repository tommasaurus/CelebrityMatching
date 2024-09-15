import psycopg2

def connect_to_db():
    """Create a new database connection."""
    return psycopg2.connect(
        host="127.0.0.1",
        port="5432",
        database="celebrity",  # Update if your database name is different
        user="root",           # Ensure this is the correct username
        password="rootpassword"  # Ensure this is the correct password
    )

def setup_celebrity_database():
    # Establish a database connection
    conn = connect_to_db()
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

    # Close the connection
    cursor.close()
    conn.close()

    print("Celebrity database has been set up.")

def setup_onlyfans_database():
    # Establish a database connection
    conn = connect_to_db()
    cursor = conn.cursor()

    # Drop the table if it exists
    cursor.execute("""
        DROP TABLE IF EXISTS onlyfans_features;
    """)
    conn.commit()

    # Create the table with the correct feature vector size
    cursor.execute("""
        CREATE TABLE onlyfans_features (
            id SERIAL PRIMARY KEY,
            img_path TEXT,
            name TEXT,
            feature_vector VECTOR(1000)  -- Adjust this column type to match the output vector size
        );
    """)
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

    print("Onlyfans database has been set up.")

if __name__ == "__main__":
    setup_celebrity_database()
    setup_onlyfans_database()
