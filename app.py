from flask import Flask, jsonify, render_template, request, session, make_response
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "help-desk-secret-key"

users = [
    {
        "id": 1,
        "username": "demo",
        "password": "demo123"
    }
]

tickets = [
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
]

VALID_CATEGORIES = {
    "Account",
    "Hardware",
    "Software",
    "Network",
    "Other"
}

VALID_PRIORITIES = {
    "Low",
    "Medium",
    "High"
}

VALID_STATUSES = {
    "Open",
    "In Progress",
    "Resolved"
}


def next_ticket_id():
    if not tickets:
        return 1
    return max(ticket["id"] for ticket in tickets) + 1


def find_ticket(ticket_id):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    return None


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return function(*args, **kwargs)

    return wrapper


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({
            "error": "Username and password are required"
        }), 400

    if any(user["username"] == username for user in users):
        return jsonify({
            "error": "Username already exists"
        }), 409

    user = {
        "id": len(users) + 1,
        "username": username,
        "password": password
    }

    users.append(user)

    return jsonify({
        "message": "Registration successful",
        "username": username
    }), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = next(
        (
            user for user in users
            if user["username"] == username
            and user["password"] == password
        ),
        None
    )

    if not user:
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    session["username"] = username

    return jsonify({
        "message": "Login successful",
        "username": username
    })


@app.route("/api/me")
def current_user():
    if "username" not in session:
        return jsonify({
            "authenticated": False
        })

    return jsonify({
        "authenticated": True,
        "username": session["username"]
    })


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "message": "Logged out successfully"
    })


@app.route("/api/tickets", methods=["GET"])
@login_required
def get_tickets():
    status = request.args.get("status")
    priority = request.args.get("priority")
    mine = request.args.get("mine")

    results = tickets

    if status:
        results = [
            ticket for ticket in results
            if ticket["status"] == status
        ]

    if priority:
        results = [
            ticket for ticket in results
            if ticket["priority"] == priority
        ]

    if mine == "true":
        results = [
            ticket for ticket in results
            if ticket["created_by"] == session["username"]
        ]

    return jsonify(results)


@app.route("/api/tickets/<int:ticket_id>", methods=["GET"])
@login_required
def get_ticket(ticket_id):
    ticket = find_ticket(ticket_id)

    if not ticket:
        return jsonify({
            "error": "Ticket not found"
        }), 404

    return jsonify(ticket)


@app.route("/api/tickets", methods=["POST"])
@login_required
def create_ticket():
    data = request.get_json() or {}

    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    category = data.get("category")
    priority = data.get("priority")

    if not title or not description:
        return jsonify({
            "error": "Title and description are required"
        }), 400

    if category not in VALID_CATEGORIES:
        return jsonify({
            "error": "Invalid category"
        }), 400

    if priority not in VALID_PRIORITIES:
        return jsonify({
            "error": "Invalid priority"
        }), 400

    ticket = {
        "id": next_ticket_id(),
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "status": "Open",
        "created_by": session["username"]
    }

    tickets.append(ticket)

    return jsonify(ticket), 201


@app.route("/api/tickets/<int:ticket_id>", methods=["PATCH"])
@login_required
def update_ticket(ticket_id):
    ticket = find_ticket(ticket_id)

    if not ticket:
        return jsonify({
            "error": "Ticket not found"
        }), 404

    data = request.get_json() or {}

    if "title" in data:
        ticket["title"] = data["title"].strip()

    if "description" in data:
        ticket["description"] = data["description"].strip()

    if "category" in data:
        if data["category"] not in VALID_CATEGORIES:
            return jsonify({
                "error": "Invalid category"
            }), 400
        ticket["category"] = data["category"]

    if "priority" in data:
        if data["priority"] not in VALID_PRIORITIES:
            return jsonify({
                "error": "Invalid priority"
            }), 400
        ticket["priority"] = data["priority"]

    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            return jsonify({
                "error": "Invalid status"
            }), 400
        ticket["status"] = data["status"]

    return jsonify(ticket)


@app.route("/api/tickets/<int:ticket_id>", methods=["DELETE"])
@login_required
def delete_ticket(ticket_id):
    ticket = find_ticket(ticket_id)

    if not ticket:
        return jsonify({
            "error": "Ticket not found"
        }), 404

    tickets.remove(ticket)

    return jsonify({
        "message": "Ticket deleted successfully"
    })


@app.route("/api/preferences", methods=["GET"])
def get_preferences():
    return jsonify({
        "ticket_filter": request.cookies.get(
            "ticket_filter",
            "all"
        )
    })


@app.route("/api/preferences", methods=["POST"])
def save_preferences():
    data = request.get_json() or {}
    ticket_filter = data.get("ticket_filter", "all")

    response = make_response(jsonify({
        "message": "Preference saved",
        "ticket_filter": ticket_filter
    }))

    response.set_cookie(
        "ticket_filter",
        ticket_filter,
        max_age=60 * 60 * 24 * 30
    )

    return response


@app.route("/api/request-info")
def request_info():
    return jsonify({
        "method": request.method,
        "path": request.path,
        "args": request.args,
        "cookies": request.cookies,
        "user_agent": request.headers.get("User-Agent")
    })


@app.route("/api/stats")
@login_required
def stats():
    total = len(tickets)

    open_count = sum(
        1 for ticket in tickets
        if ticket["status"] == "Open"
    )

    in_progress = sum(
        1 for ticket in tickets
        if ticket["status"] == "In Progress"
    )

    resolved = sum(
        1 for ticket in tickets
        if ticket["status"] == "Resolved"
    )

    return jsonify({
        "total": total,
        "open": open_count,
        "in_progress": in_progress,
        "resolved": resolved
    })


if __name__ == "__main__":
    app.run(debug=True)