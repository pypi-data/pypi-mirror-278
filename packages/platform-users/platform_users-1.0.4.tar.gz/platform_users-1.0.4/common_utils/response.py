#Python Imports


#Django Imports
from django.http import JsonResponse


#Third-Party Imports


#Project-Specific Imports


#Relative Import

class CustomResponseBuilder:
    def __init__(self):
        """Initialize the response data and status."""
        self.response_data = {}
        self.status = 200

    def set_data(self, data):
        """Set the data component of the response."""
        if data is not None:
            self.response_data["data"] = data
        return self

    def get_data(self):
        """Get the data component of the response."""
        return self.response_data.get("data")

    def set_messages(self, messages):
        """Set the messages component of the response."""
        if messages:
            self.response_data["messages"] = messages
        return self

    def get_messages(self):
        """Get the messages component of the response."""
        return self.response_data.get("messages")

    def set_errors(self, errors):
        """Set the errors component of the response."""
        if errors:
            self.response_data["errors"] = errors
        return self

    def get_errors(self):
        """Get the errors component of the response."""
        return self.response_data.get("errors")

    def set_status(self, status):
        """Set the status component of the response."""
        self.status = status
        self.response_data["status"] = self.status
        return self

    def get_status(self):
        """Get the status component of the response."""
        return self.status

    def create_response(self):
        """Create a JSON response using the response data and status."""
        return JsonResponse(self.response_data, status=self.status)

class CustomResponse:
    @staticmethod
    def success_response(data=None, messages=None, http_status=200):
        """
        Create a success response with optional custom data and messages.

        Args:
            data (dict, optional): A dictionary containing custom data. Default is None.
            messages (dict, optional): A dictionary containing custom messages. Default is None.
            http_status (int, optional): The HTTP status code. Default is 200 (OK).

        Returns:
            JsonResponse: A JSON response with the specified data, messages, and status code.
        """
        response = CustomResponseBuilder().set_status(http_status).set_data(data).set_messages(messages).create_response()
        return response

    @staticmethod
    def error_response(errors=None, http_status=400):
        """
        Create an error response with optional custom errors and a specified HTTP status code.

        Args:
            errors (list, optional): A list of error messages. Default is None.
            http_status (int, optional): The HTTP status code. Default is 400 (Bad Request).

        Returns:
            JsonResponse: A JSON response with the specified errors and status code.
        """
        response = CustomResponseBuilder().set_status(http_status).set_errors(errors).create_response()
        return response

