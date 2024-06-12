import base64
import json
import random
import string
import uuid
import re
from datetime import datetime
from uuid import UUID

from django.db.models import Model
from django.core.files import File
from django.db.models.fields.files import FieldFile

from rest_framework.response import Response
from rest_framework import serializers








def file_to_blob(file_path):
    """
    Converts a file at the given file path to a base64-encoded string.

    Args:
        file_path (str): The absolute path to the file to convert.

    Returns:
        A base64-encoded string of the file contents, or None if the file could not be found.
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            encoded_data = base64.b64encode(data).decode('utf-8')
            return encoded_data
    except FileNotFoundError:
        return None





def generate_random_username(length=8):
    """Generate a random username."""
    characters = string.ascii_letters + string.digits
    username = ''.join(random.choice(characters) for _ in range(length))
    return username

def generate_random_password(length=12):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password




def genrate_unique_number():
    # Generate a unique UUID (Universally Unique Identifier)
    unique_id = uuid.uuid4()

    # Convert the UUID to a string and remove hyphens to create a unique number
    unique_number = str(unique_id).replace('-', '')

    return unique_number


def generate_otp():
    # Generate the first digit (1-9) and append it to the OTP
    otp = str(random.randint(1, 9))

    # Generate the remaining 5 digits
    otp += ''.join([str(random.randint(0, 9)) for _ in range(5)])

    return otp



# def create_django_file(filepath):
#     """
#     Creates a Django File object from the given filepath.

#     Args:
#         filepath (str): The path to the file.

#     Returns:
#         object: The created Django File object.

#     Raises:
#         FileNotFoundError: If the file is not found.
#         IOError: If an error occurs while reading the file.
#         FileObjectCreationError: If an error occurs during the process of creating the Django File object.
#     """
#     try:
#         with open(filepath, 'rb') as file:
#             # Create a Django File object
#             django_file = File(file)

#             return django_file

#     except FileNotFoundError:
#         raise FileNotFoundError("File not found.")
#     except IOError:
#         raise IOError("Error occurred while reading the file.")
#     except Exception as e:
#         raise Exception(f"Error creating Django File object: {str(e)}")


def create_django_file(filepath):
    """
    Creates a Django File object from the given filepath.

    Args:
        filepath (str): The path to the file.

    Returns:
        object: The created Django File object.

    Raises:
        FileNotFoundError: If the file is not found.
        IOError: If an error occurs while reading the file.
        FileObjectCreationError: If an error occurs during the process of creating the Django File object.
    """
    try:
        file = open(filepath, 'rb')
        django_file = File(file)
        django_file.seek(0)  # Reset the file pointer to the beginning
        return django_file

    except FileNotFoundError:
        raise FileNotFoundError("File not found.")
    except IOError:
        raise IOError("Error occurred while reading the file.")
    except Exception as e:
        raise Exception(f"Error creating Django File object: {str(e)}")



def convert_field_type(data, field, type):
    """This function takes in a data set, field name and type as parameters 
    and converts the field to the specified type."""
    # Convert the field to the specified type
    data[field] = type(data[field])
    # Return the modified data set
    return data


def generate_response(status, message=None, data=None, pagination_data=None):
    response_data = {"status": status}
    if message is not None:
        response_data["message"] = message
    if data is not None:
        response_data["data"] = data
    if pagination_data is not None:
        response_data["count"] = pagination_data
    return Response(response_data, status=status)

def generate_error_response(status=None, errors=None):
    response_data = {"status": status, "errors": errors}
    return Response(response_data, status=status)


def serialize_errors(serializer):
    errors = {}
    for field, error_msgs in serializer.errors.items():
        if isinstance(error_msgs, list):
            errors[field] = error_msgs[0]  # use the first error message
        else:
            errors[field] = error_msgs
    return {
        "error": {
            "code": 400,
            "message": errors
        }
    }


class CustomJSONEncoder(json.JSONEncoder):
    """CustomJSONEncoder class to encode objects into JSON"""
    # Override default method to convert ObjectId, datetime, FieldFile and UUID objects into strings

    def default(self, obj):
        # if isinstance(obj, ObjectId):
        #     return str(obj)  # Convert ObjectId to string
        if isinstance(obj, datetime):
            # Convert datetime to string
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, FieldFile):
            return obj.url  # Return the URL of the FieldFile object
        elif isinstance(obj, UUID):
            return str(obj)  # Convert UUID to string
        return json.JSONEncoder.default(self, obj)  # Default


class ListQuerySerializer(serializers.Serializer):
    page_number = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)





def validate_regex(value, pattern):
    """Validate if a value matches a regex pattern."""
    return bool(re.match(pattern, value))




def replace_placeholders_with_ids(data, replacements):
    """
    A function to replace placeholder values in request.data with the corresponding model's IDs.

    Args:
        data (dict): The data dictionary in which placeholders should be replaced.
        replacements (list of dict): A list of dictionaries, each containing 'model', 'attribute', 'placeholder_key', and 'id_key' keys.

    Example:
        replacements = [
            {
                'model': Endpoint,
                'attribute': 'endpoint_name',
                'placeholder_key': 'endpoint_name',
                'id_key': 'endpoint'
            },
            {
                'model': AnotherModel,
                'attribute': 'another_name',
                'placeholder_key': 'another_name',
                'id_key': 'another'
            }
        ]
        replace_placeholders_with_ids(request.data, replacements)
    """
    for replacement in replacements:
        model = replacement.get('model')
        attribute = replacement.get('attribute')
        placeholder_key = replacement.get('placeholder_key')
        id_key = replacement.get('id_key')

        if not model or not attribute or not placeholder_key or not id_key:
            raise ValueError("Each replacement dictionary must have 'model', 'attribute', 'placeholder_key', and 'id_key' keys.")

        if data.get(placeholder_key) is not None:
            # Get the placeholder value from data
            placeholder_value = data.pop(placeholder_key)
            obj = model.objects.filter(**{attribute: placeholder_value}).first()
            if obj:
                # Replace the placeholder value with the object's ID
                data[id_key] = obj.id
    return data



def replace_placeholders_with_ids_in_list(data_list, replacements):
    """
    A function to replace placeholder values in a list of dictionaries with the corresponding model's IDs.

    Args:
        data_list (list of dict): A list of dictionaries, each containing data in which placeholders should be replaced.
        replacements (list of dict): A list of dictionaries, each containing 'model', 'attribute', 'placeholder_key', and 'id_key' keys.

    Example:
        replacements = [
            {
                'model': Endpoint,
                'attribute': 'endpoint_name',
                'placeholder_key': 'endpoint_name',
                'id_key': 'endpoint'
            },
            {
                'model': AnotherModel,
                'attribute': 'another_name',
                'placeholder_key': 'another_name',
                'id_key': 'another'
            }
        ]
        replace_placeholders_with_ids_in_list(request.data, replacements)
    """
    for item in data_list:
        for replacement in replacements:
            model = replacement.get('model')
            attribute = replacement.get('attribute')
            placeholder_key = replacement.get('placeholder_key')
            id_key = replacement.get('id_key')

            if not model or not attribute or not placeholder_key or not id_key:
                raise ValueError("Each replacement dictionary must have 'model', 'attribute', 'placeholder_key', and 'id_key' keys.")

            if item.get(placeholder_key) is not None:
                # Get the placeholder value from the item
                placeholder_value = item.pop(placeholder_key)
                obj = model.objects.filter(**{attribute: placeholder_value}).first()
                if obj:
                    # Replace the placeholder value with the object's ID in the item
                    item[id_key] = obj.id
    return data_list



class DynamicData:
    """
    A class for creating dynamic objects with key-value pairs as attributes.

    Args:
        **kwargs: Key-value pairs to be assigned as object attributes.

    Example:
        data = DynamicData(name="John", age=30)
        print(data.name)  # Outputs: "John"
        print(data.age)   # Outputs: 30
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)




class AttributeMapper:
    """A class for mapping key-value pairs to attributes and converting them to a dictionary."""
    
    def __init__(self, **kwargs):
        """Initialize the AttributeMapper with key-value pairs."""
        self.attributes = kwargs

    def to_dict(self):
        """Return the stored attributes as a dictionary."""
        return self.attributes



def get_reverse_relation_fields(model: Model) -> dict:
    """
    Get the reverse relation fields of a Django model.

    Args:
        model (Model): The Django model for which to retrieve reverse relation fields.

    Returns:
        dict: A dictionary mapping reverse relation field names to their corresponding filter attributes.
    """
    return {field.attname: f'{model._meta.model_name}__{field.attname}' for field in model._meta.fields}

