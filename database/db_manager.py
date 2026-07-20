# database/db_manager.py

import sqlite3
import os

# Define paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'configvista.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')

def get_connection():
    """Establish and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    # This allows us to access columns by name (e.g., row['hostname'])
    conn.row_factory = sqlite3.Row 
    return conn

def initialize_db():
    """Initialize the database using the schema.sql file."""
    if not os.path.exists(SCHEMA_PATH):
        print(f"[-] Error: Schema file not found at {SCHEMA_PATH}")
        return

    try:
        with get_connection() as conn:
            with open(SCHEMA_PATH, 'r') as f:
                schema_script = f.read()
            
            cursor = conn.cursor()
            cursor.executescript(schema_script)
            conn.commit()
            print(f"[+] Database successfully initialized at: {DB_PATH}")
    except sqlite3.Error as e:
        print(f"[-] SQLite error during initialization: {e}")

# If this file is run directly, initialize the database
if __name__ == "__main__":
    print("Initializing ConfigVista AI Database...")
    initialize_db()