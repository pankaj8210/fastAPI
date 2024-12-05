from fastapi import FastAPI
from datetime import datetime
from google.cloud import firestore
import requests

# Initialize the FastAPI app
app = FastAPI()

# Initialize Firestore client
db = firestore.Client()

# Fake Store API base URL
FAKE_STORE_API = "https://fakestoreapi.com"

# Part 1: FastAPI Endpoints

@app.get("/hello")
def say_hello():
    return {"message": "Hello World"}

@app.post("/add")
def add_to_firestore():
    # Get current date and time
    now = datetime.now()
    data = {
        "Day of Week": now.strftime("%A"),
        "Day of Month": now.day,
        "Month": now.strftime("%b"),
        "Timestamp": now.isoformat(),
    }

    # Add data to Firestore
    doc_ref = db.collection("sigaram_test_collection").add(data)
    return {"message": "Data added successfully", "document_id": doc_ref[1].id}

# Part 2: Fake Store Wrapper API

@app.get("/products")
def list_products():
    response = requests.get(f"{FAKE_STORE_API}/products")
    return response.json()

@app.post("/cart/{item_id}")
def add_to_cart(item_id: int):
    payload = {"userId": 1, "products": [{"productId": item_id, "quantity": 1}]}
    response = requests.post(f"{FAKE_STORE_API}/carts", json=payload)
    return response.json()

@app.get("/cart")
def list_cart_items():
    response = requests.get(f"{FAKE_STORE_API}/carts/1")
    return response.json()
