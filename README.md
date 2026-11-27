# 🛒 E-Commerce Backend API

### Product Catalog & Order Management

A FastAPI project for browsing a product catalog and creating orders. It extends the original Project 8 group database exercise into a REST API with SQLAlchemy models, request validation, and interactive documentation.

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.11+ |
| API framework | FastAPI |
| ORM | SQLAlchemy 2 |
| Database | SQLite |
| Validation | Pydantic |
| Local development | Uvicorn |
| Tests | unittest, HTTPX, GitHub Actions |

## 🚀 Key Features

- Browse the product catalog with pagination.
- Create sellers, products, customers, and orders with an API key.
- Preserve the product price on each order item at purchase time.
- Validate prices, quantities, and record IDs before saving.
- Explore request and response schemas in Swagger UI.

## 📂 Project Structure

```text
sqlalchemy_1/
├── main.py                  # FastAPI routes and request schemas
├── models.py                # SQLAlchemy models and relationships
├── database.py              # Database engine and session handling
├── requirements.txt         # Application dependencies
├── requirements-test.txt    # Test dependencies
└── tests/
    └── test_api.py           # API integration tests
```

## 🔗 REST API Endpoints

| Method | Path | Access | Description |
|---|---|---|---|
| GET | `/health` | Public | Check application status |
| GET | `/products` | Public | List products using `offset` and `limit` |
| POST | `/sellers` | API key | Create a seller |
| POST | `/products` | API key | Add a product for a seller |
| POST | `/customers` | API key | Create a customer |
| POST | `/orders` | API key | Create an order with one or more items |
| GET | `/docs` | Public | Open Swagger UI |

## ⚙️ Local Development

Run these commands in PowerShell.

```powershell
git clone https://github.com/Zuhriddin07-01/sqlalchemy_1.git
cd sqlalchemy_1
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:SHOP_WRITE_API_KEY = .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(32))"
$env:SHOP_WRITE_API_KEY
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open [Swagger UI](http://127.0.0.1:8000/docs). Copy the key printed in PowerShell and enter it under **Authorize** to use the write endpoints. Keep the key out of commits.

The app creates missing tables in `shop.db` on startup. Use a fresh local SQLite database if you have an incompatible schema from an earlier exercise, and keep a backup of the old file.

### Try the order flow

1. Create a seller and use its returned ID to add a product.
2. Create a customer and keep the returned ID.
3. Submit an order using the returned customer and product IDs. For example, if both IDs are `1`:

```json
{
  "customer_id": 1,
  "items": [{"product_id": 1, "quantity": 2}]
}
```

## 🧪 Automated Tests

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The tests use fresh SQLite databases and cover the order flow, API-key permissions, input validation, conflicts, and OpenAPI documentation.

## 👨‍💻 Author

**Zuhriddin Nosirov** · [GitHub profile](https://github.com/Zuhriddin07-01)

The original database exercise was developed with Project 8 group students.
