import os
import unittest
from contextlib import AsyncExitStack
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from httpx import ASGITransport, AsyncClient
from sqlalchemy.orm import Session

import main
from database import get_db, make_engine


WRITE_KEY = "a" * 48


class ApiTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        resources = await self.enterAsyncContext(AsyncExitStack())
        directory = Path(resources.enter_context(TemporaryDirectory()))
        self.engine = make_engine(f"sqlite:///{(directory / 'test.db').as_posix()}")
        resources.callback(self.engine.dispose)
        resources.enter_context(patch.object(main, "engine", self.engine))
        resources.enter_context(patch.dict(os.environ, SHOP_WRITE_API_KEY=WRITE_KEY))

        async def test_db():
            with Session(self.engine) as session:
                yield session

        resources.enter_context(patch.dict(main.app.dependency_overrides, {get_db: test_db}))
        await resources.enter_async_context(main.app.router.lifespan_context(main.app))
        self.client = await resources.enter_async_context(
            AsyncClient(transport=ASGITransport(app=main.app), base_url="http://testserver")
        )

    async def post(self, path, payload):
        return await self.client.post(path, json=payload, headers={"X-API-Key": WRITE_KEY})

    async def test_public_routes_and_openapi(self):
        self.assertEqual((await self.client.get("/health")).json(), {"status": "ok"})
        self.assertEqual((await self.client.get("/products")).json(), [])
        self.assertEqual((await self.client.get("/docs")).status_code, 200)
        paths = (await self.client.get("/openapi.json")).json()["paths"]
        self.assertEqual(paths["/orders"]["post"]["security"], [{"APIKeyHeader": []}])

    async def test_every_write_requires_a_valid_key(self):
        requests = {
            "/sellers": {"name": "Demo seller"},
            "/products": {"name": "Demo item", "seller_id": 1, "price": "12.50"},
            "/customers": {"first_name": "Demo", "last_name": "User", "username": "demo"},
            "/orders": {"customer_id": 1, "items": [{"product_id": 1, "quantity": 2}]},
        }
        for path, payload in requests.items():
            for headers in ({}, {"X-API-Key": "wrong"}):
                with self.subTest(path=path, headers=headers):
                    self.assertEqual((await self.client.post(path, json=payload, headers=headers)).status_code, 401)

    async def test_writes_are_unavailable_without_configuration(self):
        with patch.dict(os.environ, SHOP_WRITE_API_KEY=""):
            self.assertEqual((await self.post("/sellers", {"name": "Demo seller"})).status_code, 503)
            self.assertEqual((await self.client.get("/health")).status_code, 200)

    async def test_order_flow_and_validation(self):
        seller = await self.post("/sellers", {"name": "Demo seller"})
        self.assertEqual(seller.status_code, 201)
        product_data = {"name": "Demo item", "seller_id": seller.json()["id"], "price": "12.50"}
        product = await self.post("/products", product_data)
        self.assertEqual(product.status_code, 201)
        self.assertEqual((await self.client.get("/products?limit=1")).json(), [product.json()])
        for params in ("limit=0", "limit=101", "offset=-1", "offset=999999999999999999999"):
            self.assertEqual((await self.client.get(f"/products?{params}")).status_code, 422)
        self.assertEqual((await self.post("/products", {**product_data, "seller_id": 999})).status_code, 404)
        self.assertEqual((await self.post("/products", {**product_data, "seller_id": 2**63})).status_code, 422)

        customer_data = {"first_name": "Demo", "last_name": "User", "username": "demo"}
        customer = await self.post("/customers", customer_data)
        self.assertEqual(customer.status_code, 201)
        self.assertEqual((await self.post("/customers", customer_data)).status_code, 409)

        order_data = {
            "customer_id": customer.json()["id"],
            "items": [{"product_id": product.json()["id"], "quantity": 2}],
        }
        order = await self.post("/orders", order_data)
        self.assertEqual(order.status_code, 201)
        self.assertEqual(order.json()["status"], "pending")
        self.assertEqual(order.json()["items"][0]["unit_price"], "12.50")
        order_data["items"][0]["quantity"] = 0
        self.assertEqual((await self.post("/orders", order_data)).status_code, 422)
