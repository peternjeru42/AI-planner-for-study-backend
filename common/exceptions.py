import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        view_name = context.get("view").__class__.__name__ if context.get("view") else "unknown-view"
        request = context.get("request")
        method = getattr(request, "method", "unknown-method")
        path = getattr(request, "path", "unknown-path")
        logger.exception("Unhandled API exception in %s %s (%s)", method, path, view_name)
        return Response(
            {"success": False, "message": "Internal server error.", "errors": {"detail": ["Unexpected error."]}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    message = "Validation failed." if response.status_code < 500 else "Request failed."
    response.data = {
        "success": False,
        "message": message,
        "errors": response.data,
    }
    return response
