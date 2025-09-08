import os
import requests
from fastmcp import FastMCP, tools

API_BASE = os.getenv("API_BASE", "https://apistore-8kfz.onrender.com")
API_TOKEN = os.getenv("API_TOKEN", "mysecrettoken123")

app = FastMCP("customer-api-mcp", host="0.0.0.0",port=10000)

def call_api(path: str, method="GET", json=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    url = f"{API_BASE}{path}"
    resp = requests.request(method, url, headers=headers, json=json)
    resp.raise_for_status()
    return resp.json()

# ---- TOOLS ---- #

@app.tool()
def list_customers() -> list:
    """Get all customers."""
    return call_api("/customers")

@app.tool()
def get_customer(customer_id: str) -> dict:
    """Get a single customer by ID."""
    return call_api(f"/customers/{customer_id}")

@app.tool()
def list_orders() -> list:
    """Get all orders."""
    return call_api("/orders")

@app.tool()
def create_order(customer_id: str, product_id: str, quantity: int) -> dict:
    """Create a new order."""
    return call_api("/orders", method="POST", json={
        "customer_id": customer_id,
        "product_id": product_id,
        "quantity": quantity
    })

@app.tool()
def list_addresses() -> list:
    """Get all addresses."""
    return call_api("/addresses")

@app.tool()
def list_products() -> list:
    """Get all products."""
    return call_api("/products")

@app.tool()
def get_full_customer(customer_id: str) -> dict:
    """Get customer with related addresses and orders."""
    customer = call_api(f"/customers/{customer_id}")
    addresses = call_api(f"/addresses?customer_id={customer_id}")
    orders = call_api(f"/orders?customer_id={customer_id}")
    return {**customer, "addresses": addresses, "orders": orders}

# ---- ENTRYPOINT ---- #
if __name__ == "__main__":
    app.run(transport="streamable-http")
