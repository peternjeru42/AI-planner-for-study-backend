from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
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
