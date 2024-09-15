import subprocess

def migrate_celebrity():
    try:
        # Run migrate_celebrity.py
        print("Running migrate_celebrity.py...")
        subprocess.run(['python', 'app/db/migrate/migrate_celebrity.py'], check=True)
        print("Migration completed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the migrations: {e}")

def migrate_onlyfans():
    try:        
        # Run migrate_onlyfans.py
        print("Running migrate_onlyfans.py...")
        subprocess.run(['python', 'app/db/migrate/migrate_onlyfans.py'], check=True)
        print("Migration completed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the migrations: {e}")

if __name__ == "__main__":
    migrate_celebrity()
    migrate_onlyfans()
