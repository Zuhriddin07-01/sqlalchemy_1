import os
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
tmp = tempfile.TemporaryDirectory()
os.environ["DATABASE_URL"] = "sqlite:///" + str(Path(tmp.name) / "test.db")
from fastapi.testclient import TestClient
from main import app

def test_order_flow():
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
        seller = client.post("/sellers", json={"name":"Demo seller"})
        assert seller.status_code == 201
        product = client.post("/products", json={"name":"Demo item","seller_id":seller.json()["id"],"price":"12.50"})
        assert product.status_code == 201
        assert client.get("/products").status_code == 200
        customer = client.post("/customers", json={"first_name":"Demo","last_name":"User","username":"demo"})
        assert customer.status_code == 201
        data = {"customer_id":customer.json()["id"],"items":[{"product_id":product.json()["id"],"quantity":2}]}
        order = client.post("/orders", json=data)
        assert order.status_code == 201
        assert order.json()["items"][0]["unit_price"] == "12.50"
        data["items"][0]["quantity"] = 0
        assert client.post("/orders", json=data).status_code == 422
        assert client.post("/products",json={"name":"Invalid","seller_id":99999,"price":"1.00"}).status_code == 404
