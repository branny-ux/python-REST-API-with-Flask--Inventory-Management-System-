
import requests

from display import display_items, display_message

BASE_URL = "http://127.0.0.1:5000"


def api_request(method, path, **kwargs):
    try:
        response = requests.request(
            method,
            f"{BASE_URL}{path}",
            timeout=5,
            **kwargs,
        )
        try:
            data = response.json()
        except ValueError:
            data = {"error": response.text or "Invalid server response"}
        return response.status_code, data
    except requests.RequestException:
        display_message("Could not connect to the API. Is app.py running?")
        return None, None


def run_cli():
    while True:
        print("\nRETAIL STORE STOCK MANAGEMENT")
        print("1. View all inventory")
        print("2. View one item")
        print("3. Add an item")
        print("4. Update an item")
        print("5. Delete an item")
        print("6. Fetch product by barcode")
        print("7. Search products by name")
        print("8. Fetch and save a product by barcode")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        if choice == "1":
            status, data = api_request("GET", "/inventory")
            if status == 200:
                display_items(data)

        elif choice == "2":
            item_id = input("Item ID: ").strip()
            status, data = api_request("GET", f"/inventory/{item_id}")
            if status == 200:
                display_items([data])
            elif data:
                display_message(data.get("error", "Request failed"))

        elif choice == "3":
            name = input("Product name: ").strip()
            category = input("Category: ").strip() or "General"
            price = input("Price: ").strip()
            quantity = input("Quantity: ").strip()

            try:
                payload = {
                    "product_name": name,
                    "category": category,
                    "price": float(price),
                    "quantity": int(quantity),
                }
            except ValueError:
                print("Price must be numeric and quantity must be a whole number.")
                continue

            status, data = api_request(
                "POST", "/inventory", json=payload
            )
            display_message(data if status is None else str(data))

        elif choice == "4":
            item_id = input("Item ID: ").strip()
            print("Enter the fields to change. Leave unchanged fields blank.")
            payload = {}

            name = input("New product name: ").strip()
            category = input("New category: ").strip()
            price = input("New price: ").strip()
            quantity = input("New quantity: ").strip()

            if name:
                payload["product_name"] = name
            if category:
                payload["category"] = category

            try:
                if price:
                    payload["price"] = float(price)
                if quantity:
                    payload["quantity"] = int(quantity)
            except ValueError:
                print("Price and quantity must be valid numbers.")
                continue

            status, data = api_request(
                "PATCH", f"/inventory/{item_id}", json=payload
            )
            display_message(data if status is None else str(data))

        elif choice == "5":
            item_id = input("Item ID: ").strip()
            status, data = api_request("DELETE", f"/inventory/{item_id}")
            display_message(data if status is None else str(data))

        elif choice == "6":
            barcode = input("Barcode: ").strip()
            status, data = api_request(
                "GET", f"/inventory/fetch/barcode/{barcode}"
            )
            display_message(data if status is None else str(data))

        elif choice == "7":
            name = input("Product name: ").strip()
            status, data = api_request(
                "GET", f"/inventory/fetch/name/{name}"
            )
            display_message(data if status is None else str(data))

        elif choice == "8":
            barcode = input("Barcode: ").strip()
            status, data = api_request(
                "POST", f"/inventory/fetch/barcode/{barcode}/save"
            )
            display_message(data if status is None else str(data))

        else:
            print("Invalid option. Please choose again.")


if __name__ == "__main__":
    run_cli()