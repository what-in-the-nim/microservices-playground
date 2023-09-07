import sqlite3


def create_database(path: str) -> None:
    # Create or connect to the SQLite database
    conn = sqlite3.connect(path)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Define SQL statement to create the "orders" table
    create_orders_table = """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        product_ids TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at DATE DEFAULT CURRENT_TIMESTAMP
    );
    """

    # Execute the SQL statements to create the "orders" and "order_items" tables
    cursor.execute(create_orders_table)

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()
