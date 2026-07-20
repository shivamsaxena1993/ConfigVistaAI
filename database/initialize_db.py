"""
initialize_db.py

Initializes the ConfigVista AI SQLite database using schema.sql.
Run this script only when creating a new database or after schema changes.
"""

import sqlite3
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "configvista.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def initialize_database():
    """Create the SQLite database using schema.sql"""

    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema file not found: {SCHEMA_PATH}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            schema = schema_file.read()

        cursor.executescript(schema)

        conn.commit()
        conn.close()

        print("=" * 50)
        print("ConfigVista AI Database Initialized Successfully")
        print("=" * 50)
        print(f"Database : {DB_PATH}")
        print(f"Schema   : {SCHEMA_PATH.name}")

    except sqlite3.Error as err:
        print(f"SQLite Error : {err}")

    except Exception as ex:
        print(f"Unexpected Error : {ex}")


if __name__ == "__main__":
    initialize_database()