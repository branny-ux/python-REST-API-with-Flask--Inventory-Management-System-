
items = []
next_id = 1


def get_all_items():
    return items


def get_item(item_id):
    for item in items:
        if item["id"] == item_id:
            return item
    return None


def add_item(data):
    global next_id

    item = {
        "id": next_id,
        "product_name": data["product_name"].strip(),
        "category": data.get("category", "General"),
        "price": float(data.get("price", 0)),
        "quantity": int(data.get("quantity", 0)),
    }

    items.append(item)
    next_id += 1
    return item


def update_item(item_id, data):
    item = get_item(item_id)

    if item is None:
        return None

    if "product_name" in data:
        item["product_name"] = data["product_name"].strip()

    if "category" in data:
        item["category"] = data["category"]

    if "price" in data:
        item["price"] = float(data["price"])

    if "quantity" in data:
        item["quantity"] = int(data["quantity"])

    return item


def delete_item(item_id):
    item = get_item(item_id)

    if item is None:
        return False

    items.remove(item)
    return True


def reset_inventory():
    global next_id
    items.clear()
    next_id = 1