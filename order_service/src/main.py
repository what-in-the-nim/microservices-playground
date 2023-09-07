import os
import sqlite3

from fastapi import FastAPI

from .model import Order, OrderStatus

DATABASE_PATH = os.getenv("DATABASE_PATH")
if not os.path.exists(DATABASE_PATH):
    from .database import create_database

    create_database(DATABASE_PATH)

app = FastAPI()


def get_new_order_id():
    """
    Get a new order ID.
    """
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    cursor.execute("SELECT MAX(order_id) FROM orders")
    max_id = cursor.fetchone()[0]
    cursor.close()
    database.close()

    return 1 if max_id is None else max_id + 1


@app.post("/orders/order")
def create_order(customer_id: int, product_ids: list[int]):
    """
    Create a new order with details and return an order ID and status.
    """
    # Randomly generate an order ID
    order_id = get_new_order_id()
    # Create a new order with the ID
    order = Order(id=order_id, customer_id=customer_id, product_ids=product_ids)
    # Save the order to the database
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    cursor.execute(
        "INSERT INTO orders (order_id, customer_id, product_ids, status, created_at) VALUES (?, ?, ?, ?, ?)",
        order.tuple,
    )
    database.commit()
    cursor.close()
    database.close()
    # Return the order ID and status
    return {"id": order_id, "status": order.status}


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    """Get an order by ID."""
    # Retrieve the order from the database
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()
    # Return an error if the order does not exist
    if order is None:
        return {"error": "Order does not exist"}
    # Return the order
    order = Order.from_tuple(order)
    cursor.close()
    database.close()
    return order


@app.get("/orders/user/{customer_id}")
def get_customer_orders(customer_id: int):
    """
    Get all orders for a customer.
    """
    # Retrieve customer orders from the database
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
    orders = cursor.fetchall()
    # Return an error if the customer has no orders
    if orders is None:
        return {"error": "No orders found"}
    # Return the orders
    orders = [Order.from_tuple(order) for order in orders]
    cursor.close()
    database.close()
    return orders


@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, status: OrderStatus):
    """
    Update the status of an order.
    """
    assert status in OrderStatus, "Invalid order status"
    # Update the order status in the database
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    # Find the order
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()
    # Return an error if the order does not exist
    if order is None:
        return {"error": "Order does not exist"}

    cursor.execute(
        "UPDATE orders SET status = ? WHERE order_id = ?", (status, order_id)
    )
    database.commit()
    cursor.close()
    database.close()
    # Return the order ID and status
    return {"id": order_id, "status": status}


@app.delete("/orders/{order_id}")
def cancel_order(order_id: int):
    """Cancel an order."""
    # Retrieve the order from the database
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()
    # Return an error if the order does not exist
    if order is None:
        return {"error": "Order does not exist"}

    order = Order.from_tuple(order)
    # Check if the order is cancellable
    if order.status == OrderStatus.cancelled:
        return {"message": "Order already cancelled"}
    elif order.status == OrderStatus.delivered:
        return {"message": "Order already delivered"}
    # Update the order status in the database
    cursor.execute(
        "UPDATE orders SET status = ? WHERE order_id = ?",
        (OrderStatus.cancelled, order_id),
    )
    database.commit()
    cursor.close()
    database.close()
    # Return the order ID and status
    return {"id": order_id, "status": OrderStatus.cancelled}


@app.get("/orders")
def get_orders():
    """Get all orders (admin only)."""
    # Retrieve the orders from the database
    database = sqlite3.connect(DATABASE_PATH)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    if orders is None:
        return {"error": "No orders found"}

    # Return the orders
    orders = [Order.from_tuple(order) for order in orders]
    cursor.close()
    database.close()
    return orders
