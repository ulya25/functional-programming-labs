from core import Order, make_processor

order1: Order = {
    "id": 1,
    "items": [{"name": "Pizza", "price": 150.0, "qty": 2}],
    "paid": False,
}
order2: Order = {
    "id": 2,
    "items": [{"name": "Coffee", "price": 50.0, "qty": 3}],
    "paid": True,
}
order3: Order = {
    "id": 3,
    "items": [{"name": "Tiramisu", "price": 200.0, "qty": 2}],
    "paid": True,
}
order4: Order = {
    "id": 4,
    "items": [{"name": "Vine", "price": 320.0, "qty": 1}],
    "paid": True,
}
orders = [order1, order2, order3, order4]

accent = lambda s: s >= 200
apply_discount = lambda s: s * 0.9
apply_service = lambda s: s * 1.1

processor = make_processor(
    accept=accent, apply_discount=apply_discount, apply_service=apply_service
)


def render_report(result):
    for o in result["orders"]:
        print("Order", o["id"], "total:", o["total"])
    print("Count:", result["count"])
    print("Revenue:", result["revenue"])


if __name__ == "__main__":
    result = processor(orders)
    render_report(result)
