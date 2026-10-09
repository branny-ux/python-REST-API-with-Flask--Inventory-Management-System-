# Retail Store Stock Management API

A Flask REST API with a command-line client for managing retail store inventory. The application supports CRUD operations, stock tracking, and product lookup through the OpenFoodFacts API.

## Features

* Create, view, update, and delete inventory items.
* Track product names, categories, prices, and quantities.
* Fetch product information by barcode or name.
* Fetch products from OpenFoodFacts and save them to inventory.
* Interactive terminal-based CLI client.
* Automated pytest suite with mocked external HTTP requests.
* In-memory inventory storage.

## Project Structure

```text
inventory-management-system/
├── app.py
├── cli.py
├── display.py
├── inventory.py
├── external_api.py
├── requirements.txt
├── README.md
└── tests/
    ├── __init__.py
    ├── test_app.py
    └── test_external_api.py
```

## Requirements

* Python 3
* Flask
* requests
* pytest

## Installation

Clone the repository or open the existing project folder in VS Code.

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

On Windows, activate the environment using:

```bash
venv\Scripts\activate
```

## Running the Application

Open two VS Code terminals and activate the virtual environment in each.

Terminal 1 — Start the Flask API:

```bash
python app.py
```

Terminal 2 — Start the CLI client:

```bash
python cli.py
```

The API runs at:

`http://127.0.0.1:5000`

## API Endpoints

| Method | Endpoint                                  | Description              |
| ------ | ----------------------------------------- | ------------------------ |
| GET    | `/`                                       | API welcome message      |
| GET    | `/inventory`                              | List all items           |
| GET    | `/inventory/<id>`                         | Retrieve one item        |
| POST   | `/inventory`                              | Create an item           |
| PATCH  | `/inventory/<id>`                         | Update an item           |
| DELETE | `/inventory/<id>`                         | Delete an item           |
| GET    | `/inventory/fetch/barcode/<barcode>`      | Fetch product by barcode |
| GET    | `/inventory/fetch/name/<name>`            | Search products by name  |
| POST   | `/inventory/fetch/barcode/<barcode>/save` | Fetch and save a product |

## Example Requests

View inventory:

```bash
curl http://127.0.0.1:5000/inventory
```

Add an item:

```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name":"Rice","category":"Groceries","price":150,"quantity":10}'
```

Update an item's price:

```bash
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price":175}'
```

Delete an item:

```bash
curl -X DELETE http://127.0.0.1:5000/inventory/1
```

Fetch a product by barcode:

```bash
curl http://127.0.0.1:5000/inventory/fetch/barcode/3017620422003
```

## CLI Menu

The terminal client provides these options:

1. View all inventory
2. View one item
3. Add an item
4. Update an item
5. Delete an item
6. Fetch product by barcode
7. Search products by name
8. Fetch and save a product by barcode
9. Exit

## Testing

Run the automated tests:

```bash
pytest -v
```

The tests cover inventory CRUD operations, input validation, API errors, and mocked OpenFoodFacts requests.

The test suite is designed to run without making real network requests.

## Technology Stack

* Python
* Flask
* Requests
* Pytest
* OpenFoodFacts API
* In-memory data storage

## Limitations

Inventory data is held in memory and is cleared when the application restarts. A future version could use SQLite or PostgreSQL for persistent storage.

## Author

Developed as a Python REST API and CLI inventory management project by Branis Beru.
