from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from django.db import transaction  # type: ignore
from .models import Order, OrderItem


@dataclass
class OrderItemRequest:
    product_name: str
    quantity: int
    price: Decimal


@dataclass
class OrderRequest:
    user: Any
    items: list[OrderItemRequest]


@transaction.atomic
def create_order(order_request: OrderRequest) -> Order:
    order = Order.objects.create(user=order_request.user)

    total = Decimal("0.00")

    for item in order_request.items:
        OrderItem.objects.create(
            order=order,
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price,
        )
        total += item.price * item.quantity

    order.total_amount = total
    order.save()

    return order
