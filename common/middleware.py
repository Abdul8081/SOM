import uuid
import logging

logger = logging.getLogger(__name__)

class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        request.request_id = request_id

        response = self.get_response(request)

        response["X-Request-ID"] = request_id
        logger.info(
            f"{request.method} {request.path} | {response.status_code} | {request_id}"
        )
        return response
