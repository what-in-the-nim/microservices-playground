import sqlite3
from datetime import datetime


def create_database(path: str) -> None:
    # Create a SQLite database or connect to an existing one
    conn = sqlite3.connect(path)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Define SQL statements to create tables
    create_products_table = """
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        price DECIMAL(10, 2),
        quantity INTEGER,
        description TEXT,
        created_at DATE,
        updated_at DATE
    );
    """

    # Execute the SQL statements to create tables
    cursor.execute(create_products_table)

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()


def add_products(path: str) -> None:
    # Create a SQLite database or connect to an existing one
    conn = sqlite3.connect(path)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    flowers = [
        ("Red Roses", 29.99, 100, "A dozen red roses"),
        ("White Roses", 29.99, 100, "A dozen white roses"),
        ("Orchids", 24.99, 100, "A dozen orchids"),
        ("Tulips", 19.99, 100, "A dozen tulips"),
        ("Sunflowers", 14.99, 100, "A dozen sunflowers"),
        ("Daisies", 9.99, 100, "A dozen daisies"),
        ("Carnations", 9.99, 100, "A dozen carnations"),
        ("Daffodils", 9.99, 100, "A dozen daffodils"),
        ("Dahlias", 9.99, 100, "A dozen dahlias"),
        ("Lilies", 9.99, 100, "A dozen lilies"),
        ("Peonies", 9.99, 100, "A dozen peonies"),
        ("Ranunculus", 9.99, 100, "A dozen ranunculus"),
        ("Anemones", 9.99, 100, "A dozen anemones"),
        ("Gardenias", 9.99, 100, "A dozen gardenias"),
        ("Hydrangeas", 9.99, 100, "A dozen hydrangeas"),
        ("Lilacs", 9.99, 100, "A dozen lilacs"),
        ("Marigolds", 9.99, 100, "A dozen marigolds"),
        ("Peonies", 9.99, 100, "A dozen peonies"),
        ("Roses", 9.99, 100, "A dozen roses"),
    ]

    # Add products
    for idx, flower in enumerate(flowers):
        current_datetime = datetime.now()
        cursor.execute(
            "INSERT INTO products (product_id, product_name, price, quantity, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                idx + 1,
                flower[0],
                flower[1],
                flower[2],
                flower[3],
                current_datetime,
                current_datetime,
            ),
        )

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()
