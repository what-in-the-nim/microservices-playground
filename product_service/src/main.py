import logging
import os
import sqlite3
from typing import Optional

from fastapi import FastAPI

from .model import Product

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

app = FastAPI()


def get_new_product_id():
    """Get a new product ID."""
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    cursor.execute("SELECT MAX(product_id) FROM products")
    max_id = cursor.fetchone()[0]
    cursor.close()
    database.close()
    return 1 if max_id is None else max_id + 1


@app.get("/products")
def get_products():
    """Get all products (admin only)."""
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    # If there are no products, return an empty list
    logging.info(f"Products: {products}")
    if products is None:
        return []

    products = [Product.from_tuple(product) for product in products]

    cursor.close()
    database.close()
    return products


@app.post("/products/add")
def add_product(
    name: str, price: float, quantity: int, description: Optional[str] = None
):
    """
    Add a new product with details and return a product ID.
    """
    # Randomly generate a product ID
    product_id = get_new_product_id()
    # Create a new product with the ID
    product = Product(
        id=product_id,
        name=name,
        price=price,
        quantity=quantity,
        description=description,
    )
    # Save the product to the database
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    cursor.execute(
        "INSERT INTO products (product_id, product_name, price, quantity, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        product.tuple,
    )
    database.commit()
    cursor.close()
    database.close()
    # Return the product ID
    return {"id": product_id}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    """Get a product by ID."""
    # Retrieve the product from the database
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
    product = cursor.fetchone()

    # Return an error if the product does not exist
    if product is None:
        return {"error": "Product does not exist"}
    # Return the product
    product = Product.from_tuple(product)
    cursor.close()
    database.close()
    # Return the product
    return product


@app.put("/products/{product_id}/update")
def update_product(product_id: int, name: str, price: float):
    """Update a product by ID."""
    # Retrieve the product from the database
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
    product = cursor.fetchone()

    # Return an error if the product does not exist
    if product is None:
        return {"error": "Product does not exist"}

    # Save the product to the database
    cursor.execute(
        "UPDATE products SET product_name = ?, price = ? WHERE product_id = ?",
        (name, price, product_id),
    )
    database.commit()
    cursor.close()
    database.close()
    return {"id": product_id}


if __name__ == "__main__":
    from .database import add_products, create_database

    if not os.path.exists(DATABASE_PATH):
        create_database(DATABASE_PATH)
        add_products(DATABASE_PATH)
