# Inventory Management System API

A RESTful API built with **Python and Flask** for managing inventory products. The system provides endpoints for creating, viewing, updating, and deleting inventory items.

## Features

* Create inventory items
* View all inventory items
* View a single inventory item
* Update inventory items
* Delete inventory items
* JSON API responses
* Input validation
* Automated testing with Pytest

## Technologies

* Python 3
* Flask
* REST API
* Pytest
* Git
* GitHub

## Project Structure

```text
inventory-management-system/
├── app.py
├── test_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/branny-ux/python-REST-API-with-Flask--Inventory-Management-System-.git
```

Enter the project directory:

```bash
cd python-REST-API-with-Flask--Inventory-Management-System-
```

Create a virtual environment:

```bash
python3 -m venv env
```

Activate it:

```bash
source env/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the API

Start the Flask application:

```bash
python3 app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

## API Endpoints

| Method | Endpoint          | Description              |
| ------ | ----------------- | ------------------------ |
| GET    | `/inventory`      | Get all inventory items  |
| GET    | `/inventory/<id>` | Get one inventory item   |
| POST   | `/inventory`      | Create an inventory item |
| PUT    | `/inventory/<id>` | Update an inventory item |
| DELETE | `/inventory/<id>` | Delete an inventory item |

## Example POST Request

```json
{
    "name": "Laptop",
    "quantity": 10,
    "price": 75000
}
```

## Example GET Request

```bash
curl http://127.0.0.1:5000/inventory
```

## Running Tests

Run the automated tests with:

```bash
pytest
```

The tests verify that the API endpoints work correctly.

## HTTP Status Codes

| Code | Meaning            |
| ---- | ------------------ |
| 200  | Successful request |
| 201  | Resource created   |
| 400  | Bad request        |
| 404  | Resource not found |

## Future Improvements

* Add a database such as MySQL or PostgreSQL
* Add user authentication
* Add JWT authorization
* Add product categories
* Add stock-level alerts
* Add search and filtering
* Deploy the API online
* Add Swagger/OpenAPI documentation

## Author

**Branis Khagali Beru**

Kabarak University
Banking and Finance

## GitHub Repository

https://github.com/branny-ux/python-REST-API-with-Flask--Inventory-Management-System-
 python-REST-API-with-Flask--Inventory-Management-System-
