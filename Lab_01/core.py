from collections.abc import Callable, Iterable
from typing import TypedDict

FilterFn = Callable[[float], bool]
DiscountFn = Callable[[float], float]
ServiceFn = Callable[[float], float]


class Item(TypedDict):
    name: str
    price: float
    qty: int


class Order(TypedDict, total=False):
    id: int
    items: list[Item]
    paid: bool
    total: float


def order_subtotal(order: Order) -> float:
    return sum(it["price"] * it["qty"] for it in order["items"])


def with_total(order: Order, total: float) -> Order:
    return {**order, "total": total}


def process_orders_pure(
    orders: Iterable[Order], *, min_total: float, discount: float, service_rate: float
) -> dict[str, object]:
    paid = (o for o in orders if o["paid"])
    qualified = []
    revenue = 0.0
    for o in paid:
        subtotal = order_subtotal(o)
        if subtotal < min_total:
            continue
        total = subtotal * (1 - discount) * (1 + service_rate)
        new_o = with_total(o, total)
        revenue += total
        qualified.append(new_o)
    return {"count": len(qualified), "revenue": revenue, "orders": qualified}


def make_processor(
    *, accept: FilterFn, apply_discount: DiscountFn, apply_service: ServiceFn
) -> Callable[[list[Order]], dict[str, object]]:
    def process(orders: list[Order]) -> dict[str, object]:
        qualified = []
        revenue = 0.0
        for o in orders:
            if not o["paid"]:
                continue
            subtotal = order_subtotal(o)
            if not accept(subtotal):
                continue
            total = apply_service(apply_discount(subtotal))
            qualified.append(with_total(o, total))
            revenue += total
        return {"count": len(qualified), "revenue": revenue, "orders": qualified}

    return process
