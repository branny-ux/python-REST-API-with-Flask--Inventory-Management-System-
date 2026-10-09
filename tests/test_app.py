
import pytest

import app as application
import inventory


@pytest.fixture
def client():
    inventory.reset_inventory()
    application.app.config["TESTING"] = True
    with application.app.test_client() as test_client:
        yield test_client
    inventory.reset_inventory()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json


def test_list_empty_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.json == []


def test_create_item(client):
    response = client.post("/inventory", json={
        "product_name": "Rice",
        "category": "Groceries",
        "price": 150,
        "quantity": 10,
    })
    assert response.status_code == 201
    assert response.json["product_name"] == "Rice"


def test_create_item_requires_name(client):
    response = client.post("/inventory", json={"price": 20})
    assert response.status_code == 400


def test_create_item_rejects_invalid_json(client):
    response = client.post(
        "/inventory",
        data="not json",
        content_type="application/json",
    )
    assert response.status_code == 400


def test_get_existing_item(client):
    created = client.post(
        "/inventory", json={"product_name": "Milk"}
    )
    item_id = created.json["id"]
    response = client.get(f"/inventory/{item_id}")
    assert response.status_code == 200
    assert response.json["product_name"] == "Milk"


def test_get_missing_item(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404


def test_patch_item(client):
    created = client.post(
        "/inventory", json={"product_name": "Bread", "price": 50}
    )
    item_id = created.json["id"]
    response = client.patch(
        f"/inventory/{item_id}", json={"price": 65}
    )
    assert response.status_code == 200
    assert response.json["price"] == 65


def test_patch_missing_item(client):
    response = client.patch("/inventory/999", json={"price": 20})
    assert response.status_code == 404


def test_patch_rejects_empty_data(client):
    created = client.post(
        "/inventory", json={"product_name": "Soap"}
    )
    response = client.patch(
        f"/inventory/{created.json['id']}", json={}
    )
    assert response.status_code == 400


def test_delete_item(client):
    created = client.post(
        "/inventory", json={"product_name": "Sugar"}
    )
    item_id = created.json["id"]
    response = client.delete(f"/inventory/{item_id}")
    assert response.status_code == 200
    assert client.get(f"/inventory/{item_id}").status_code == 404


def test_delete_missing_item(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404


def test_fetch_barcode(client, monkeypatch):
    monkeypatch.setattr(
        application.external_api,
        "fetch_by_barcode",
        lambda barcode: {
            "product_name": "Chocolate",
            "category": "Snacks",
            "brands": "Example",
            "barcode": barcode,
        },
    )
    response = client.get("/inventory/fetch/barcode/12345")
    assert response.status_code == 200
    assert response.json["product_name"] == "Chocolate"


def test_fetch_name(client, monkeypatch):
    monkeypatch.setattr(
        application.external_api,
        "fetch_by_name",
        lambda name: [
            {"product_name": name, "category": "Food",
             "brands": "", "barcode": "123"}
        ],
    )
    response = client.get("/inventory/fetch/name/rice")
    assert response.status_code == 200
    assert response.json[0]["product_name"] == "rice"


def test_fetch_barcode_not_found(client, monkeypatch):
    monkeypatch.setattr(
        application.external_api,
        "fetch_by_barcode",
        lambda barcode: None,
    )
    response = client.get("/inventory/fetch/barcode/000")
    assert response.status_code == 404


def test_fetch_service_error(client, monkeypatch):
    def fail(barcode):
        raise application.external_api.requests.RequestException("offline")

    monkeypatch.setattr(
        application.external_api, "fetch_by_barcode", fail
    )
    response = client.get("/inventory/fetch/barcode/123")
    assert response.status_code == 502


def test_fetch_and_save(client, monkeypatch):
    monkeypatch.setattr(
        application.external_api,
        "fetch_by_barcode",
        lambda barcode: {
            "product_name": "Tea",
            "category": "Drinks",
            "brands": "Example",
            "barcode": barcode,
        },
    )
    response = client.post("/inventory/fetch/barcode/456/save")
    assert response.status_code == 201
    assert response.json["product_name"] == "Tea"
    assert response.json["barcode"] == "456"