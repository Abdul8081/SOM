from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from django.db import transaction  # type: ignore
from .models import Order, OrderItem
from notifications.tasks import send_order_created_notification
from django.core.cache import cache
import logging
logger = logging.getLogger(__name__)


@dataclass
class OrderItemRequest:
    name: str
    quantity: int
    price: Decimal


@dataclass
class OrderRequest:
    user: Any
    items: list[OrderItemRequest]


@transaction.atomic
def create_order(*, user, items):
    with transaction.atomic():
        order = Order.objects.create(user=user)

        total = Decimal("0.00")

        for item in items:
            # line_total = item["price"] * item["quantity"]   in this line therew was the error, item an object not dictionary, I was using that in the form of the dictionary that's why this issue was coming.  like payment = 0.0. and item = 0.
            line_total = item.price * item.quantity
            total += line_total

            OrderItem.objects.create(
                order=order,
                name=item.name,
                price=item.price,
                quantity=item.quantity,
            )

        order.total_amount = total
        order.save(update_fields=["total_amount"])
        
        logger.info(
            f"Order created: order_id={order.id}, user_id={user.id}, total={total}"
        )
        
         # 🔥 CACHE INVALIDATION
        cache.delete(f"user_orders_{user.id}")
        cache.delete(f"latest_order_{user.id}")
        
        send_order_created_notification.delay(order.user.id, order.id)

        return order
