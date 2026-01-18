def order_created_message(order_id):
    return ("Order Created", f"Your order #{order_id} has been created successfully.")


def payment_success_message(order_id, amount):
    return (
        "Payment Successful",
        f"Payment received for Order #{order_id}. Amount: ₹{amount}",
    )
