
import requests

BASE_URL = "https://world.openfoodfacts.org/api/v2"


def extract_fields(product):
    return {
        "product_name": product.get("product_name", ""),
        "category": product.get("categories", "General"),
        "brands": product.get("brands", ""),
        "barcode": product.get("code", ""),
    }


def fetch_by_barcode(barcode):
    response = requests.get(
        f"{BASE_URL}/product/{barcode}.json",
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("status") != 1 or not data.get("product"):
        return None

    return extract_fields(data["product"])


def fetch_by_name(name):
    response = requests.get(
        f"{BASE_URL}/search",
        params={
            "search_terms": name,
            "json": 1,
            "page_size": 10,
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    return [
        extract_fields(product)
        for product in data.get("products", [])
        if product.get("product_name")
    ]