import uuid


class MockPaymentProvider:
    def initiate(self, amount):
        return {
            "transaction_id": str(uuid.uuid4()),
            "provider_payment_id": str(uuid.uuid4()),
            "status": "PENDING",
        }

    def confirm(self, provider_payment_id):
        # Always succeed for now
        return {
            "status": "SUCCESS",
            "provider_payment_id": provider_payment_id,
        }
