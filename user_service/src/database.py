import os
import sqlite3

from dotenv import load_dotenv

from .model import User

load_dotenv()


def create_database(path: str) -> None:
    # Create a SQLite database or connect to an existing one
    conn = sqlite3.connect(path)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Define SQL statement to create the "users" table
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        is_admin BOOLEAN NOT NULL DEFAULT 0,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP NOT NULL
    );
    """

    # Execute the SQL statement to create the "users" table
    cursor.execute(create_users_table)

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()


def add_admin(path: str) -> None:
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
    password_hash = User.get_password_hash(ADMIN_PASSWORD)

    admin = User(
        id=1,
        username=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        password_hash=password_hash,
        is_admin=True,
    )

    # Add an admin user
    cursor.execute(
        "INSERT INTO users (user_id, username, email, password_hash, is_admin, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        admin.tuple(return_password=True),
    )

    conn.commit()
    conn.close()
