
from flask import Flask, jsonify, request

import external_api
import inventory

app = Flask(__name__)


def validate_item(data, partial=False):
    if not isinstance(data, dict):
        return "Request body must be a JSON object"

    if not partial and not str(data.get("product_name", "")).strip():
        return "product_name is required"

    if "product_name" in data:
        if not isinstance(data["product_name"], str):
            return "product_name must be text"
        if not data["product_name"].strip():
            return "product_name cannot be empty"

    if "category" in data and not isinstance(data["category"], str):
        return "category must be text"

    if "price" in data:
        try:
            price = float(data["price"])
            if price < 0:
                return "price cannot be negative"
        except (TypeError, ValueError):
            return "price must be a number"

    if "quantity" in data:
        try:
            quantity = int(data["quantity"])
            if isinstance(data["quantity"], bool):
                return "quantity must be a whole number"
            if quantity != float(data["quantity"]) or quantity < 0:
                return "quantity must be a non-negative whole number"
        except (TypeError, ValueError, OverflowError):
            return "quantity must be a whole number"

    return None


@app.get("/")
def home():
    return jsonify({
        "message": "Retail Store Stock Management API",
        "endpoints": "/inventory",
    })


@app.get("/inventory")
def list_inventory():
    return jsonify(inventory.get_all_items()), 200


@app.get("/inventory/<int:item_id>")
def get_inventory_item(item_id):
    item = inventory.get_item(item_id)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item), 200


@app.post("/inventory")
def create_inventory_item():
    data = request.get_json(silent=True)
    error = validate_item(data)

    if error:
        return jsonify({"error": error}), 400

    item = inventory.add_item(data)
    return jsonify(item), 201


@app.patch("/inventory/<int:item_id>")
def patch_inventory_item(item_id):
    data = request.get_json(silent=True)
    error = validate_item(data, partial=True)

    if error:
        return jsonify({"error": error}), 400

    if not data:
        return jsonify({"error": "Update data is required"}), 400

    item = inventory.update_item(item_id, data)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item), 200


@app.delete("/inventory/<int:item_id>")
def remove_inventory_item(item_id):
    if not inventory.delete_item(item_id):
        return jsonify({"error": "Item not found"}), 404

    return jsonify({"message": "Item deleted"}), 200


@app.get("/inventory/fetch/barcode/<barcode>")
def fetch_barcode(barcode):
    try:
        product = external_api.fetch_by_barcode(barcode)
    except (external_api.requests.RequestException, ValueError):
        return jsonify({"error": "Product service unavailable"}), 502

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200


@app.get("/inventory/fetch/name/<path:name>")
def fetch_name(name):
    try:
        products = external_api.fetch_by_name(name)
    except (external_api.requests.RequestException, ValueError):
        return jsonify({"error": "Product service unavailable"}), 502

    return jsonify(products), 200


@app.post("/inventory/fetch/barcode/<barcode>/save")
def fetch_and_save(barcode):
    try:
        product = external_api.fetch_by_barcode(barcode)
    except (external_api.requests.RequestException, ValueError):
        return jsonify({"error": "Product service unavailable"}), 502

    if not product:
        return jsonify({"error": "Product not found"}), 404

    item_data = {
        "product_name": product["product_name"],
        "category": product["category"],
        "price": 0,
        "quantity": 0,
    }

    item = inventory.add_item(item_data)
    item["barcode"] = product["barcode"]
    item["brands"] = product["brands"]

    return jsonify(item), 201


if __name__ == "__main__":
    app.run(debug=True)