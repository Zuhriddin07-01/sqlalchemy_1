from contextlib import asynccontextmanager
from decimal import Decimal
from os import getenv
from secrets import compare_digest
from typing import Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Query, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import Seller, Product, Customer, Order, OrderItem

@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(title="E-Commerce API", version="1.0.0", lifespan=lifespan)
DB = Annotated[Session, Depends(get_db)]
write_api_key = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_write_key(key: Annotated[str | None, Security(write_api_key)]):
    expected = getenv("SHOP_WRITE_API_KEY", "")
    if len(expected) < 32 or not expected.isascii():
        raise HTTPException(503, "Write access is unavailable")
    if key is None or not compare_digest(key.encode(), expected.encode()):
        raise HTTPException(
            401, "A valid API key is required", headers={"WWW-Authenticate": "APIKey"}
        )


write_access = [Depends(require_write_key)]
RecordId = Annotated[int, Field(gt=0, le=2**63 - 1)]

class SellerIn(BaseModel):
    name: str = Field(min_length=1, max_length=50)

class SellerOut(SellerIn):
    model_config = ConfigDict(from_attributes=True)
    id: int

class ProductIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    seller_id: RecordId
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)

class ProductOut(ProductIn):
    model_config = ConfigDict(from_attributes=True)
    id: int

class CustomerIn(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=200)
    username: str = Field(min_length=1, max_length=100)

class CustomerOut(CustomerIn):
    model_config = ConfigDict(from_attributes=True)
    id: int

class ItemIn(BaseModel):
    product_id: RecordId
    quantity: int = Field(gt=0, le=10000)

class OrderIn(BaseModel):
    customer_id: RecordId
    items: list[ItemIn] = Field(min_length=1, max_length=100)

class ItemOut(ItemIn):
    model_config = ConfigDict(from_attributes=True)
    unit_price: Decimal

class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_number: str
    customer_id: int
    status: str
    items: list[ItemOut]

def save(db, obj):
    db.add(obj)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Database constraint conflict")
    db.refresh(obj)
    return obj

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/sellers", response_model=SellerOut, status_code=201, dependencies=write_access)
def create_seller(data: SellerIn, db: DB):
    return save(db, Seller(**data.model_dump()))

@app.post("/products", response_model=ProductOut, status_code=201, dependencies=write_access)
def create_product(data: ProductIn, db: DB):
    if db.get(Seller, data.seller_id) is None:
        raise HTTPException(404, "Seller not found")
    return save(db, Product(**data.model_dump()))

@app.get("/products", response_model=list[ProductOut])
def products(
    db: DB,
    offset: Annotated[int, Query(ge=0, le=2147483647)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
):
    return list(db.scalars(select(Product).order_by(Product.id).offset(offset).limit(limit)))

@app.post("/customers", response_model=CustomerOut, status_code=201, dependencies=write_access)
def create_customer(data: CustomerIn, db: DB):
    return save(db, Customer(**data.model_dump()))

@app.post("/orders", response_model=OrderOut, status_code=201, dependencies=write_access)
def create_order(data: OrderIn, db: DB):
    if db.get(Customer, data.customer_id) is None:
        raise HTTPException(404, "Customer not found")
    order = Order(customer_id=data.customer_id, order_number=str(uuid4()), status="pending")
    for item in data.items:
        product = db.get(Product, item.product_id)
        if product is None:
            raise HTTPException(404, "Product not found")
        order.items.append(OrderItem(product_id=product.id, quantity=item.quantity, unit_price=product.price))
    return save(db, order)
