
def display_items(items):
    if not items:
        print("No inventory items found.")
        return

    print(f"{'ID':<5} {'Product':<25} {'Category':<18} {'Price':>10} {'Quantity':>10}")
    print("-" * 75)

    for item in items:
        print(
            f"{item['id']:<5} "
            f"{item['product_name'][:24]:<25} "
            f"{item['category'][:17]:<18} "
            f"{item['price']:>10.2f} "
            f"{item['quantity']:>10}"
        )


def display_message(message):
    print(message)