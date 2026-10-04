import pytest

from app import app, users, tickets


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_data():
    users.clear()
    users.append({
        "id": 1,
        "username": "demo",
        "password": "demo123"
    })

    tickets.clear()
    tickets.extend([
        {
            "id": 1,
            "title": "Cannot access email",
            "description": "My university email is not opening.",
            "category": "Account",
            "priority": "High",
            "status": "Open",
            "created_by": "demo"
        },
        {
            "id": 2,
            "title": "Printer not working",
            "description": "The office printer is not responding.",
            "category": "Hardware",
            "priority": "Medium",
            "status": "In Progress",
            "created_by": "demo"
        }
    ])


def login(client):
    return client.post(
        "/api/login",
        json={
            "username": "demo",
            "password": "demo123"
        }
    )


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"SupportHub" in response.data


def test_register(client):
    response = client.post(
        "/api/register",
        json={
            "username": "newuser",
            "password": "password123"
        }
    )

    assert response.status_code == 201


def test_login(client):
    response = login(client)

    assert response.status_code == 200


def test_current_user(client):
    login(client)

    response = client.get("/api/me")

    assert response.status_code == 200
    assert response.json["authenticated"] is True


def test_auth_required(client):
    response = client.get("/api/tickets")

    assert response.status_code == 401


def test_create_ticket(client):
    login(client)

    response = client.post(
        "/api/tickets",
        json={
            "title": "New problem",
            "description": "Something is not working.",
            "category": "Software",
            "priority": "Low"
        }
    )

    assert response.status_code == 201
    assert response.json["title"] == "New problem"


def test_update_ticket(client):
    login(client)

    response = client.patch(
        "/api/tickets/1",
        json={
            "status": "Resolved"
        }
    )

    assert response.status_code == 200
    assert response.json["status"] == "Resolved"


def test_delete_ticket(client):
    login(client)

    response = client.delete("/api/tickets/1")

    assert response.status_code == 200


def test_cookie_preference(client):
    response = client.post(
        "/api/preferences",
        json={
            "ticket_filter": "open"
        }
    )

    assert response.status_code == 200

    response = client.get("/api/preferences")

    assert response.json["ticket_filter"] == "open"


def test_request_inspector(client):
    response = client.get("/api/request-info")

    assert response.status_code == 200
    assert response.json["method"] == "GET"