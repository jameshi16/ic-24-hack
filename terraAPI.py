from fastapi import FastAPI
from pymongo import MongoClient
import requests

app = FastAPI()
#
base_url = "http://127.0.0.1:8000"

dev_id = ""
api_key = ""


@app.get("/app")
async def root():
    client = MongoClient(
        "mongodb+srv://mertal:ichack123@cluster0.f74h5dy.mongodb.net/?retryWrites=true&w=majority"
    )

    db = client["Cluster0"]
    collection = db["activity"]

    all_items = []
    for item in collection.find({}):
        all_items.append(item)

    return {"message": all_items}


@app.get("/login")
async def auth():
    res = requests.post(
        "https://api.tryterra.co/auth/generateWidgetSession",
        headers={"dev-id": dev_id, "x-api-key": api_key},
        json={
            "reference_id": "john",
            "auth_succes_redirect_url": f"{base_url}/success",
        },
    )
