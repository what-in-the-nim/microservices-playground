import logging
import os
import sqlite3

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .model import User

# Configure logging to write logs to a file and stream to the console
logging.basicConfig(
    filename="app.log",  # Log file
    format="%(asctime)s [%(levelname)s]: %(message)s",
    level=logging.INFO,
)

# Create a handler to stream logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter for the console logs
console_formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
console_handler.setFormatter(console_formatter)

# Add the console handler to the root logger
root_logger = logging.getLogger()
root_logger.addHandler(console_handler)

DATABASE_PATH = os.getenv("DATABASE_PATH")
if not os.path.exists(DATABASE_PATH):
    from .database import add_admin, create_database

    create_database(DATABASE_PATH)
    add_admin(DATABASE_PATH)


app = FastAPI()


def get_new_user_id():
    """Get a new user ID."""
    database = sqlite3.connect(DATABASE_PATH)
    logging.info("Connected to database")
    cursor = database.cursor()
    cursor.execute("SELECT MAX(user_id) FROM users")
    max_id = cursor.fetchone()[0]
    logging.info(f"Max ID: {max_id}")
    cursor.close()
    database.close()
    return 1 if max_id is None else max_id + 1


@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}

@app.get("/users")
def get_users():
    """Get all users (admin only)."""
    database = sqlite3.connect(DATABASE_PATH)
    logging.info("Connected to database")
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    logging.info(f"Users: {users}")
    cursor.close()
    database.close()
    return users


@app.post("/users/register")
def register(username: str, email: str, password: str):
    """
    Create a new user with details and return a user ID.
    """
    # Randomly generate a user ID
    user_id = get_new_user_id()
    # Create a new user with the ID
    password_hash = User.get_password_hash(password)

    logging.info(f"User ID: {user_id}")
    logging.info(f"Username: {username}")
    logging.info(f"Email: {email}")
    logging.info(f"Password Hash: {password_hash}")

    user = User(id=user_id, username=username, email=email, password_hash=password_hash)
    logging.info(f"is_admin: {user.is_admin}")
    # Save the user to the database
    logging.info("Connecting to database")
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    # Find if the user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    if existing_user is not None:
        return {"error": "User already exists"}
    # Insert the user into the database
    cursor.execute(
        "INSERT INTO users (user_id, username, email, password_hash, is_admin, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        user.tuple(return_password=True),
    )
    database.commit()
    cursor.close()
    database.close()
    # Return the JSON response
    return JSONResponse(content={"message": "Register completed"}, status_code=200)


@app.post("/users/login")
def login(username: str, password: str):
    """
    Login a user and return a user ID.
    """
    # Retrieve the user from the database
    logging.info("Login request")
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    logging.info(f"Login found user: {user}")
    cursor.close()
    database.close()

    # Check if the user exists
    if user is None:
        logging.info(f"User: {username} not found")
        return JSONResponse(content={"error": "User not found"}, status_code=404)

    logging.info("User: found")
    user = User.from_tuple(user)
    logging.info(f"User: {user}")

    # Check if the password is correct
    if User.get_password_hash(password) != user.password_hash:
        logging.info(f"Incorrect password for {user.username}")
        return JSONResponse(content={"error": "Incorrect password"}, status_code=401)

    # Return the user ID
    logging.info(f"Successfully logged in as {user.username} ({user.id})")
    return JSONResponse(
        content={"message": "Login completed", "is_admin": user.is_admin},
        status_code=200,
    )
