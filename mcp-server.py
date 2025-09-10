# mcp_server.py
from fastmcp import FastMCP
import requests
import os

# ========================
# Configuration
# ========================
#API_BASE = os.getenv("API_BASE", "http://localhost:8000")  # Replace with deployed API URL if needed
API_BASE = os.getenv("API_BASE", "https://apistore-8kfz.onrender.com")
API_TOKEN = os.getenv("API_TOKEN", "rnd_c4JQDWayMxdPliDy5I2KLTlaoOIK")

def call_api(path, method="GET", data=None, params=None):
    url = f"{API_BASE}{path}"
    if method.upper() == "GET":
        resp = requests.get(url, params=params)
    elif method.upper() == "POST":
        resp = requests.post(url, json=data)
    elif method.upper() == "PATCH":
        resp = requests.patch(url, json=data)
    elif method.upper() == "DELETE":
        resp = requests.delete(url)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")
    resp.raise_for_status()
    return resp.json() if resp.content else {"success": True}

# ========================
# FastMCP App
# ========================
app = FastMCP("customer-api-mcp", host="0.0.0.0",port=10000)

# ========================
# Customers
# ========================
@app.tool()
def list_customers() -> list:
    """Retrieve all customers."""
    return call_api("/customers")

@app.tool()
def get_customer_details(customer_id: str) -> dict:
    """Get full details of a customer including addresses and orders."""
    return call_api(f"/customers/{customer_id}/details")

@app.tool()
def create_customer(customer_data: dict) -> dict:
    """Create a new customer."""
    return call_api("/customers", method="POST", data=customer_data)

@app.tool()
def update_customer(customer_id: str, update_data: dict) -> dict:
    """Update an existing customer by ID."""
    return call_api(f"/customers/{customer_id}", method="PATCH", data=update_data)

@app.tool()
def delete_customer(customer_id: str) -> dict:
    """Delete a customer by ID."""
    return call_api(f"/customers/{customer_id}", method="DELETE")

# ========================
# Addresses
# ========================
@app.tool()
def list_addresses() -> list:
    """Retrieve all addresses."""
    return call_api("/addresses")

@app.tool()
def create_address(address_data: dict) -> dict:
    """Create a new address."""
    return call_api("/addresses", method="POST", data=address_data)

@app.tool()
def update_address(address_id: str, update_data: dict) -> dict:
    """Update an address by ID."""
    return call_api(f"/addresses/{address_id}", method="PATCH", data=update_data)

@app.tool()
def delete_address(address_id: str) -> dict:
    """Delete an address by ID."""
    return call_api(f"/addresses/{address_id}", method="DELETE")

# ========================
# Orders
# ========================
@app.tool()
def list_orders() -> list:
    """Retrieve all orders."""
    return call_api("/orders")

@app.tool()
def create_order(order_data: dict) -> dict:
    """Create a new order."""
    return call_api("/orders", method="POST", data=order_data)

@app.tool()
def update_order(order_id: str, update_data: dict) -> dict:
    """Update an order by ID."""
    return call_api(f"/orders/{order_id}", method="PATCH", data=update_data)

@app.tool()
def delete_order(order_id: str) -> dict:
    """Delete an order by ID."""
    return call_api(f"/orders/{order_id}", method="DELETE")

# ========================
# Products
# ========================
@app.tool()
def list_products() -> list:
    """Retrieve all products."""
    return call_api("/products")

@app.tool()
def create_product(product_data: dict) -> dict:
    """Create a new product."""
    return call_api("/products", method="POST", data=product_data)

@app.tool()
def update_product(product_id: str, update_data: dict) -> dict:
    """Update a product by ID."""
    return call_api(f"/products/{product_id}", method="PATCH", data=update_data)

@app.tool()
def delete_product(product_id: str) -> dict:
    """Delete a product by ID."""
    return call_api(f"/products/{product_id}", method="DELETE")

# ========================
# Run MCP server
# ========================
if __name__ == "__main__":
    print("Starting MCP server for Customer API...")
    app.run(transport="streamable-http")

