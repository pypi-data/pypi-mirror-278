#Python Imports
import configparser
import os
from dataclasses import dataclass, field
from typing import Optional, List, Set, Tuple

#Django Imports

#Third-Party Imports

#Project-Specific Imports

#Relative Import

def load_error_messages(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    
    error_messages = {}
    
    for section in config.sections():
        for key, value in config.items(section):
            error_messages[key.upper()] = value
    
    return error_messages


# Get the directory of the current module
current_dir = os.path.dirname(os.path.abspath(__file__))

# Path to your message.properties file within the package
MESSAGE_PROPERTIES_FILE_PATH = os.path.join(current_dir, 'error_messages.properties')



# # Path to your message.properties file
# MESSAGE_PROPERTIES_FILE_PATH = 'error_messages.properties'

# Load the error messages
error_messages = load_error_messages(MESSAGE_PROPERTIES_FILE_PATH)

# Create a function to retrieve error messages by error code
def get_error_message(error_code):
    return error_messages.get(error_code, 'Undefined error')





@dataclass
class V2stechErrorMessage:
    """
    Data class for representing a message with a message code and message text.

    Attributes:
    - message_code (str): The code associated with the message. Default is None.
    - message (str): The message text. Default is None.
    """
    error_code: str = None
    error_message: str = None

    def to_dict(self):
        """
        Convert the message object to a dictionary. If values are None, set default values.

        Returns:
        dict: A dictionary with keys 'message_code' and 'message'.
        """
        return {"error_code": self.error_code or "UNDEFINED_CODE", "error_message": self.error_message or "UNDEFINED_MESSAGE"}

@dataclass
class V2stechErrorMessageHandler:
    """
    Class for handling messages.

    Attributes:
    - messages (List[V2stechErrorMessage]): A list of message objects.
    """
    errors: List[V2stechErrorMessage] = field(default_factory=list)

    def add_message(self, error_code, error_message):
        """
        Add a message to the message list.

        Args:
        - message_code (str): The code associated with the message.
        - message (str): The message text.
        """
        error_message_obj = V2stechErrorMessage(error_code, error_message).to_dict()
        self.errors.append(error_message_obj)

    def get_messages(self):
        """
        Get the list of errors.

        Returns:
        List[V2stechErrorMessage]: A list of message objects.
        """
        return self.errors

