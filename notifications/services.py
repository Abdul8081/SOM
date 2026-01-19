def order_created_message(order_id: int):
    subject = "Order Created Successfully"
    message = f"""
Your order has been placed successfully!

Order ID: {order_id}

Thank you for shopping with us.
"""
    return subject, message


def payment_success_message(order_id: int, amount):
    subject = "Payment Successful"
    message = f"""
Your payment was successful!

Order ID: {order_id}
Amount Paid: ₹{amount}

Thank you for your purchase.
"""
    return subject, message
