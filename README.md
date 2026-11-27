# E-Commerce Backend API

An educational group project (Project 8), extended from the original SQLAlchemy database exercise into a local FastAPI API.

## Stack
Python, FastAPI, SQLAlchemy 2, SQLite, Pydantic, Uvicorn, pytest.

## Features
- Seller, product, customer, order and order item models.
- Foreign key enforcement, price and quantity constraints, unique order numbers.
- Product listing with pagination.
- Order creation with stored unit prices.
- Request validation and database conflict handling.
- Interactive OpenAPI documentation.

## Quick start
Use Python 3.10+ in a virtual environment.

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs

## Routes
| Method | Path | Purpose |
|---|---|---|
| GET | /health | Application status |
| POST | /sellers | Create seller |
| POST | /products | Create product |
| GET | /products | List products |
| POST | /customers | Create customer |
| POST | /orders | Create order |

Create a seller first, then a product and customer, then an order referencing their IDs.

## Database
Seller 1:N Product; Customer 1:N Order; Order 1:N OrderItem; Product 1:N OrderItem.

SQLite is the default. DATABASE_URL can override the connection string. Tables are created on startup. Existing incompatible databases require a migration or a fresh development database; back up existing data first.

## Tests
```bash
python -m pytest -q
```

## Scope
Local demonstration only. Authentication, authorization, inventory, payment processing, migrations and production security are not implemented. Do not expose this API publicly or use real customer data. Tests are provided but execution has not been verified in this environment.

## Attribution
Originally developed with Project 8 group students.
