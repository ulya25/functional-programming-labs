from copy import deepcopy

import pytest

from core import Order, make_processor, process_orders_pure


@pytest.fixture
def sample_orders() -> list[Order]:
    return [
        {
            "id": 1,
            "items": [{"name": "Pizza", "price": 150.0, "qty": 2}],
            "paid": False,
        },
        {"id": 2, "items": [{"name": "Coffee", "price": 50.0, "qty": 3}], "paid": True},
        {
            "id": 3,
            "items": [{"name": "Tiramisu", "price": 200.0, "qty": 2}],
            "paid": True,
        },
        {"id": 4, "items": [{"name": "Vine", "price": 320.0, "qty": 1}], "paid": True},
    ]


def test_referential_transparency(sample_orders: list[Order]) -> None:
    args = {"min_total": 200, "discount": 0.1, "service_rate": 0.1}
    r1 = process_orders_pure(sample_orders, **args)
    r2 = process_orders_pure(sample_orders, **args)
    assert r1 == r2


def test_no_mutation(sample_orders: list[Order]) -> None:
    original = deepcopy(sample_orders)
    process_orders_pure(sample_orders, min_total=0, discount=0.0, service_rate=0.0)
    assert sample_orders == original


def test_callable_policies(sample_orders: list[Order]) -> None:
    processor = make_processor(
        accept=lambda s: s >= 200,
        apply_discount=lambda s: s,
        apply_service=lambda s: s,
    )
    result = processor(sample_orders)
    assert result["count"] == 2
    assert result["revenue"] == pytest.approx(720.0)
