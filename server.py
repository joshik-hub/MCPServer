import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

API_BASE = os.getenv("API_BASE", "https://apistore-8kfz.onrender.com")
API_TOKEN = os.getenv("API_TOKEN", "mysecrettoken123")

app = FastAPI(title="Customer MCP Server", version="1.0.0")

def call_api(path: str, method="GET", json=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    url = f"{API_BASE}{path}"
    resp = requests.request(method, url, headers=headers, json=json)
    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()

# ---- MODELS ---- #
class OrderCreate(BaseModel):
    customer_id: str
    product_id: str
    quantity: int

# ---- ENDPOINTS (tools exposed over HTTP) ---- #

@app.get("/tools/list_customers")
@app.head("/tools/list_customers")
def list_customers():
    """Get all customers."""
    return call_api("/customers")

@app.get("/tools/get_customer/{customer_id}")
@app.head("/tools/get_customer/{customer_id}")
def get_customer(customer_id: str):
    """Get a single customer by ID."""
    return call_api(f"/customers/{customer_id}")

@app.get("/tools/list_orders")
@app.head("/tools/list_orders")
def list_orders():
    """Get all orders."""
    return call_api("/orders")

@app.post("/tools/create_order")
def create_order(order: OrderCreate):
    """Create a new order."""
    return call_api("/orders", method="POST", json=order.model_dump())

@app.get("/tools/list_addresses")
@app.head("/tools/list_addresses")
def list_addresses():
    """Get all addresses."""
    return call_api("/addresses")

@app.get("/tools/list_products")
@app.head("/tools/list_products")
def list_products():
    """Get all products."""
    return call_api("/products")

@app.get("/tools/get_full_customer/{customer_id}")
@app.head("/tools/get_full_customer/{customer_id}")
def get_full_customer(customer_id: str):
    """Get customer with related addresses and orders."""
    customer = call_api(f"/customers/{customer_id}")
    addresses = call_api(f"/addresses?customer_id={customer_id}")
    orders = call_api(f"/orders?customer_id={customer_id}")
    return {**customer, "addresses": addresses, "orders": orders}

