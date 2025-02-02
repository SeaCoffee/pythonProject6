from rest_framework.views import exception_handler
from rest_framework.response import Response

def error_handler(exc: Exception, context: dict):
    handlers = {
        "JWTException": jwt_validation_exception_handler
    }

    response = exception_handler(exc, context)
    exc_class = exc.__class__.__name__

    if exc_class in handlers:
        return handlers[exc_class](exc, context)

    return response


def jwt_validation_exception_handler(exc, context):
    return Response({'details': 'JWT expired'})

