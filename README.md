# E-Commerce Backend API

A FastAPI and SQLAlchemy portfolio project for browsing a product catalog and creating orders. It extends the original Project 8 group database exercise.

## Features

- Public product catalog with pagination and interactive Swagger documentation.
- API-key protected creation of sellers, products, customers and orders.
- Relational constraints, validated inputs and prices stored with each order item.

## Run locally

Use Python 3.11 or newer. From the repository root, run these commands in PowerShell.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:SHOP_WRITE_API_KEY = .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(32))"
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open the [local Swagger UI](http://127.0.0.1:8000/docs). Use **Authorize** with the value of `SHOP_WRITE_API_KEY` to try write endpoints. The key is a shared credential for demo operators. Keep it outside source control and use HTTPS on hosted instances. Writes return 401 for missing or incorrect keys and 503 if the server key is unavailable.

## API

| Method | Path | Access | Purpose |
|---|---|---|---|
| GET | `/health` | Public | Health check |
| GET | `/products` | Public | List products with `offset` and `limit` |
| POST | `/sellers` | API key | Create a seller |
| POST | `/products` | API key | Create a product |
| POST | `/customers` | API key | Create a customer |
| POST | `/orders` | API key | Create an order |

Create a seller, add a product for that seller, and create a customer. Then submit an order with the customer ID, product ID and quantity.

## Run tests

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Each test uses a fresh SQLite database. The suite checks permissions, the order flow, input validation, conflicts and the OpenAPI security scheme.

## Render demo

Create a Blueprint in Render and select this repository and its `main` branch. [render.yaml](render.yaml) defines the build and start commands, the `/health` check, and a generated `SHOP_WRITE_API_KEY` in Render's environment. Open `/health` and `/docs` on the URL Render assigns after the deployment succeeds.

The free demo uses SQLite in an ephemeral filesystem. Use sample data only. A restart or redeploy can erase the catalog and orders. Back up any existing local database before changing its schema. The app creates missing tables on startup.

## Attribution

Originally developed with Project 8 group students.
