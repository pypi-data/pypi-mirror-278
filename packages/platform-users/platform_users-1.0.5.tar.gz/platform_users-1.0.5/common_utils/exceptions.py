#Python Imports
from traceback import print_exc

#Django Imports

#Third-Party Imports
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

#Project-Specific Imports
from common_utils.message import STATUS_MESSAGES
from common_utils.utils import generate_response,generate_error_response

#Relative Import


class CustomException(Exception):
    """Custom exception class for handling application-specific errors."""
    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(error_message)

class CustomValidationException(APIException):
    """Custom exception class for formatting error messages."""
    def __init__(self, errors, status_code):
        self.errors = errors
        self.status_code = status_code
        super().__init__(detail=self.errors)


class V2StechValidationError:
    """Class for managing validation errors and error messages."""
    def __init__(self, error_code, error_message,status_code=status.HTTP_400_BAD_REQUEST):
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message
        self.errors = []

    def add_error(self, error_code, error_message):
        """Add a validation error with an error code and message to the error list."""
        self.errors.append(V2StechValidationError(error_code, error_message,self.status_code).to_dict())

    def to_dict(self):
        """Convert the validation error to a dictionary."""
        return {"error_code": self.error_code, "error_message": self.error_message}

    def validate(self):
        """Validate the error list and raise a CustomValidationException if errors exist."""
        if self.errors:
            raise CustomValidationException(self.errors,status_code=self.status_code)
        return True

    def add_error_and_raise(self,error_code,error_message,status_code):
        """Add error in  the error list and raise a CustomValidationException if errors exist."""
        self.errors.append(V2StechValidationError(error_code, error_message,status_code).to_dict())
        if self.errors:
            raise CustomValidationException(self.errors,status_code=self.status_code)
        return True

def handle_exception(exception):
    """
    A helper function to handle different types of exceptions and return an appropriate response.

    Args:
        exception: An exception object that needs to be handled.

    Returns:
        A Response object with an appropriate error message and status code.
    """
    if isinstance(exception, ValidationError) or isinstance(exception, NotFound):
        message = exception.detail
        return generate_response(status=status.HTTP_400_BAD_REQUEST, message=message)
    if isinstance(exception, CustomValidationException):
        errors = exception.errors
        return generate_error_response(status=exception.status_code, errors=errors)
    elif isinstance(exception, FileNotFoundError) or isinstance(exception, ValueError):
        message = str(exception)
        return generate_response(status=status.HTTP_400_BAD_REQUEST, message=message)
    elif isinstance(exception, CustomException):
        error_response = {
            "error_code": exception.error_code,
            "error_message": exception.error_message
        }
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)  # Set appropriate HTTP status code

    else:
        print_exc()
        message = STATUS_MESSAGES.get(500)
        return generate_response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=message)


