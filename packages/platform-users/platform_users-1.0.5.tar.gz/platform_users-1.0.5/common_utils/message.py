#Python Imports
import configparser
from dataclasses import dataclass, field
from typing import Optional, List, Set, Tuple

#Django Imports

#Third-Party Imports

#Project-Specific Imports

#Relative Import


@dataclass
class V2stechMessage:
    """
    Data class for representing a message with a message code and message text.

    Attributes:
    - message_code (str): The code associated with the message. Default is None.
    - message (str): The message text. Default is None.
    """
    message_code: str = None
    message: str = None

    def to_dict(self):
        """
        Convert the message object to a dictionary. If values are None, set default values.

        Returns:
        dict: A dictionary with keys 'message_code' and 'message'.
        """
        return {"message_code": self.message_code or "UNDEFINED_CODE", "message": self.message or "UNDEFINED_MESSAGE"}

@dataclass
class MessageHandler:
    """
    Class for handling messages.

    Attributes:
    - messages (List[V2stechMessage]): A list of message objects.
    """
    messages: List[V2stechMessage] = field(default_factory=list)

    def add_message(self, message_code, message):
        """
        Add a message to the message list.

        Args:
        - message_code (str): The code associated with the message.
        - message (str): The message text.
        """
        message_obj = V2stechMessage(message_code, message).to_dict()
        self.messages.append(message_obj)

    def get_messages(self):
        """
        Get the list of messages.

        Returns:
        List[V2stechMessage]: A list of message objects.
        """
        return self.messages


def load_success_messages(file_path):
    """
    Load success messages from a properties file.

    Args:
    - file_path (str): The path to the properties file.

    Returns:
    dict: A dictionary containing success messages with their associated codes.
    """
    config = configparser.ConfigParser()
    config.read(file_path)

    success_messages = {}

    for section in config.sections():
        for key, value in config.items(section):
            success_messages[key.upper()] = value

    return success_messages


# Path to your success_message.properties file
MESSAGE_PROPERTIES_FILE_PATH = 'success_messages.properties'

# Load the success messages
success_messages = load_success_messages(MESSAGE_PROPERTIES_FILE_PATH)

# Create a function to retrieve success messages by success code
def get_success_message(error_code):
    """
    Get a success message by its code.

    Args:
    - error_code (str): The code associated with the success message.

    Returns:
    str: The success message text. Returns 'UNDEFINED_MESSAGE' if the code is not found.
    """
    return success_messages.get(error_code, 'UNDEFINED_MESSAGE')



def object_not_exists_message(object_name, object_id):
    """
    Generates an error message for an item with a given ID.

    Args:
        object_name (str): The name of the item.
        object_id (str): The ID of the item.

    Returns:
        A string error message.
    """
    return f"No {object_name} exists with ID {object_id}"


MESSAGES = {
    'CREATED': '{} created successfully.',
    'RETRIEVED': '{} retrieved successfully.',
    'UPDATED': '{} updated successfully.',
    'DELETED': '{} deleted successfully.',
    'UPDATE_FAILED': 'Unable to update {}.',
    'DELETE_FAILED': 'Unable to delete {}.',
    'NO_CONTENT': 'No data found.',
    'GET_ALL': '{} retrieved successfully.',
    # ... add more messages here ...
}


STATUS_MESSAGES = {
    200: 'Ok',
    201: '{} deleted successfully.',
    204: [],
    401: "You are not authorized to access this resource. Admin access required.",
    403: "You are not allowed to perform this action.",
    404: "{} Not found with id {}",
    500: "Internal Server Error",
}


LOGGER_MSG = {
    "GET_DETAILS": 'Getting {} details for ID {}.',
    "GET_ALL": 'Getting all {} data.',
    "RETRIEVED": '{} with ID {} retrieved successfully.',
    "ERROR": "An exception occurred: {}",
    "OBJECT_NOT_FOUND": "No {} details found for ID {}",
    "CREATING": "Creating a {}.",
    "CREATED": "{} created successfully with data {}.",
    "UPDATING": "Updating {} with ID {}",
    "UPDATED": "{} with ID {} updated successfully.",
    "PARTIALLY_UPDATED": "{} with ID {} partially updated successfully.",
    "DELETING": "Deleting user with ID {}.",
    "DELETED": "{} with ID {} deleted successfully.",
    'DELETE_FAILED': 'Unable to delete {}.',
    "DATA": "{} data retrieved successfully.",
    "DATA_NOT_FOUND": "No {} data found.",
}



