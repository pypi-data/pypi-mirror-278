#Python Imports
import re
from dataclasses import dataclass, field
from typing import Optional, List, Set, Tuple
from abc import ABC, abstractmethod


#Django Imports
from django.urls import get_resolver

#Third-Party Imports

#Project-Specific Imports
from common_utils.exceptions import V2StechValidationError
from properties import USER_REGISTRATION_FEATURE

#Relative Import

from django.contrib.auth import authenticate
from django.db.models import Model


@dataclass
class FieldValidationException:
    """
    Data class for representing a validation error.

    Attributes:
    - error_code (str): The code associated with the error.
    - error_message (str): The error message text.
    """
    error_code: str
    error_message: str

@dataclass
class ValidatorBase(ABC):
    """
    Base abstract class for creating data validators.

    Attributes:
    - field_name (str): The name of the field to validate.
    - errors (List[FieldValidationException]): A list of validation errors.
    """

    field_name: Optional[str] = None
    errors: List[FieldValidationException] = field(default_factory=list)

    @abstractmethod
    def validate(self, value):
        """Validate a value and add errors to the errors list as needed."""
        pass

    def add_error(self, error_code, error_message):
        """Add a validation error to the errors list."""
        self.errors.append(FieldValidationException(error_code, error_message))

    def validate_field(self, data):
        """
        Validate a field within a data dictionary and return a list of validation errors.

        Args:
        - data (dict): The data dictionary containing the field to validate.

        Returns:
        - List[FieldValidationException]: A list of validation errors.
        """
        value = data.get(self.field_name)
        self.validate(value)
        return self.errors

@dataclass
class ValidationResult:
    """Data class for validation result."""
    is_valid: bool
    errors: List[str]

class ValidatorHelper:
    """
    Helper class for validating data and collecting errors.

    Attributes:
    - data (dict): The data to be validated.
    - validators (list): A list of validation objects.
    """

    @staticmethod
    def validate_and_collect_errors(data, validators):
        """Validate data using a list of validators and collect errors into a set of tuples (error_code, error_message)."""
        errors_set: Set[Tuple[str, str]] = set()

        for validator in validators:
            errors_set.update((error.error_code, error.error_message) for error in validator.validate_field(data))

        return errors_set

    @staticmethod
    def convert_errors_set_to_list(errors_set):
        """
        Convert a set of errors (error_code, error_message) to a list of error dictionaries.

        The resulting list is sorted by error_code.
        """
        errors = [{'error_code': code, 'error_message': message} for code, message in errors_set]
        sorted_errors = sorted(errors, key=lambda x: x["error_code"])
        return sorted_errors

@dataclass
class MinMaxLengthValidator(ValidatorBase):
    """
    Validate the length of a value based on minimum and maximum length criteria.
    """

    min_length: Optional[int] = None
    max_length: Optional[int] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):
        value = str(value)
        """Validate the length of the value based on min and max length criteria and add an error if it doesn't meet the requirements."""
        if self.min_length is not None and len(value) < self.min_length:
            self.add_error(self.error_code, self.error_message)
        if self.max_length is not None and len(value) > self.max_length:
            self.add_error(self.error_code, self.error_message)

@dataclass
class EmptyValidator(ValidatorBase):
    """
    Validator for checking if a field is empty or not based on 'allow_blank' parameter.
    """
    allow_blank: bool = False
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):
        if not self.allow_blank and not value:
            self.add_error(self.error_code, self.error_message)

@dataclass
class AlphanumericValidator(ValidatorBase):
    """
    Validator for checking if a field contains only alphanumeric characters.
    """
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):
        if not value.isalnum():
            self.add_error(self.error_code, self.error_message)


@dataclass
class AlphanumericRegixValidator(ValidatorBase):
    """
    Validator for checking if a string contains only alphanumeric characters using regex.
    """
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):
        if not isinstance(value, str):
            # Convert the value to a string
            value = str(value)
        pattern = r"^[a-zA-Z0-9]+$"
        if not re.match(pattern, value):
            self.add_error(self.error_code, self.error_message)



@dataclass
class AlphabeticRegexValidator(ValidatorBase):
    """
    Validator for checking if a string contains only alphabetical characters using regex.
    """
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):
        if not isinstance(value, str):
            # Convert the value to a string
            value = str(value)
        pattern = r"^[a-zA-Z]+$"
        if not re.match(pattern, value):
            self.add_error(self.error_code, self.error_message)


@dataclass
class UppercaseUnderscoreRegexValidator(ValidatorBase):
    """
    Validator for checking if a string is either all uppercase or uppercase and underscore-separated using regex.
    """
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):
        if not isinstance(value, str):
            # Convert the value to a string
            value = str(value)
        # Allow either all uppercase or uppercase and underscore-separated
        pattern = r"^[A-Z_]+$|^[A-Z]+$"
        if not re.match(pattern, value):
            self.add_error(self.error_code, self.error_message)


@dataclass
class AlphanumericWithWhitespaceValidator(ValidatorBase):
    """
    Validator for checking if a field contains only alphanumeric characters and whitespace.
    """
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):

        # Check if the value is an integer and convert it to a string
        if isinstance(value, int):
            self.add_error(self.error_code, self.error_message)
            value = str(value)
        # pattern = r'^[a-zA-Z0-9\s.]*$'
        pattern = r'^[a-zA-Z0-9\s._-]*$'
        if not re.match(pattern, value):
            self.add_error(self.error_code, self.error_message)



@dataclass
class AlphabeticUnderscoreHyphenValidator(ValidatorBase):
    """
    Validator for checking if a field contains only alphabets, underscores, and hyphens.
    """
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):

        # Check if the value is an integer and convert it to a string
        if isinstance(value, int):
            self.add_error(self.error_code, self.error_message)
            value = str(value)
        
        # Allow alphabets, underscores, and hyphens only
        pattern = r'^[a-zA-Z_\-]+$'

        if not re.match(pattern, value):
            self.add_error(self.error_code, self.error_message)

    def add_error(self, error_code, error_message):
        # Add your error handling logic here
        pass



@dataclass
class MobileNumberValidator(ValidatorBase):
    """
    Validator for checking if a mobile number is digit and should be exactly 10 digits long.
    """
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):
        if not isinstance(value, str):
            # Convert the integer to a string
            value = str(value)
        pattern = r"^\d{10}$"
        if not re.match(pattern, value):
            self.add_error(self.error_code, self.error_message)


@dataclass
class ZipCodeValidator(ValidatorBase):
    """
    Validator for checking if a string is a valid ZIP code.
    """
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):

        # Check if the value is an integer and convert it to a string
        if isinstance(value, int):
            self.add_error(self.error_code, self.error_message)
            value = str(value)

        # Allow 5-digit and 9-digit ZIP codes (with optional hyphen)
        pattern = r'^\d{5}(?:-\d{4})?$'

        if not re.match(pattern, value):
            self.add_error(self.error_code, self.error_message)


@dataclass
class EmailValidator(ValidatorBase):
    """
    Validator for checking if a string is a valid email address.
    """
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):
        if not isinstance(value, str):
            # Convert the value to a string
            value = str(value)
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, value):
            self.add_error(self.error_code, self.error_message)



@dataclass
class StringOnlyValidator(ValidatorBase):
    """
    Validator for checking if a field contains only string.
    """
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):
        if not isinstance(value, str):
            self.add_error(self.error_code, self.error_message)


@dataclass
class ListOfDictionariesValidator(ValidatorBase):
    """
    Validator for checking if a list contains at least one dictionary.
    """
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):
        if not isinstance(value, list) or not any(isinstance(item, dict) for item in value):
            self.add_error(self.error_code, self.error_message)



@dataclass
class DigitsOnlyValidator(ValidatorBase):
    """
    Validator for checking if a field contains only digits.
    """
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):
        # Check if the value is an integer
        if isinstance(value, int):
            self.add_error(self.error_code, self.error_message)

@dataclass
class StringDigitsOnlyValidator(ValidatorBase):
    """
    Validator for checking if a field contains only digits in string.
    """
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):
        # Check if the value is an integer (positive or negative)
        value_str = str(value)
        if not value_str.lstrip('-').isdigit():
            self.add_error(self.error_code, self.error_message)
    
@dataclass
class RegexValidator(ValidatorBase):
    """
    Validator for applying custom regular expression-based validation methods to a field.
    """
    regex_pattern: str = r'^[A-Za-z0-9]+$'
    validation_method: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):
        """Validate a value using the specified validation method."""
        if self.validation_method:
            getattr(self, self.validation_method)(value)

    def validate_mobile_number(self, value):
        """Validate a value as a mobile number."""
        regex_pattern = r"^(?=\d{10,15}$)\d+$"
        if not re.match(regex_pattern, value):
            self.add_error(self.error_code, self.error_message)

    def validate_email(self, value):
        """Validate a value as an email address."""
        regex_pattern = r'^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,4}$'
        if not re.match(regex_pattern, value):
            self.add_error(self.error_code, self.error_message)

    def validate_allow_specific_special_characters(self, value):
        """Validate a value to allow specific special characters."""
        regex_pattern = r'^[\w\s.,]+$'
        if not re.match(regex_pattern, value):
            self.add_error(self.error_code, self.error_message)

    def validate_digits_only(self, value):
        """Validate a value to contain only digits."""
        regex_pattern = r'^\d+$'
        if not re.match(regex_pattern, value):
            self.add_error(self.error_code, self.error_message)



class UnitValidator(ValidatorBase):
    """Validator for checking if a field is one of the specified valid units."""
    def __init__(self, field_name,valid_units:List[str], error_code: Optional[str] = None, error_message: Optional[str] = None):
        super().__init__(field_name)
        self.valid_units = valid_units
        self.error_code = error_code
        self.error_message = error_message

    def validate(self, value):
        if value not in self.valid_units:
            self.add_error(self.error_code, self.error_message)



class AuthPassValidator(ValidatorBase):
    """
    Validator for checking if a record with the same attribute value exists in the database.
    """
    def __init__(self, model_class: ABC, attribute_name: str, error_code: Optional[str] = None, error_message: Optional[str] = None,**kwargs: dict):
        super().__init__(attribute_name)
        self.model_class = model_class
        self.attribute_name = attribute_name
        self.error_code = error_code
        self.error_message = error_message
        self.kwargs = kwargs

    def validate(self, value=None):
        existing_record = authenticate(**self.kwargs)
        if not existing_record:
            self.add_error(self.error_code, self.error_message)


class ModelAttributeExistsValidator(ValidatorBase):
    """
    Validator for checking if a record with the same attribute value exists in the database.
    """
    def __init__(self,field_name, model_class: ABC, attribute_name: str, error_code: Optional[str] = None, error_message: Optional[str] = None):
        super().__init__(field_name)
        self.field_name = field_name
        self.model_class = model_class
        self.attribute_name = attribute_name
        self.error_code = error_code
        self.error_message = error_message

    def validate(self, value):
        filter_kwargs = {self.attribute_name: value}
        existing_record = self.model_class.objects.filter(**filter_kwargs).first()
        if existing_record:
            self.add_error(self.error_code, self.error_message)


class ModelAttributeNotExistsValidator(ValidatorBase):
    """
    Validator for checking if a record with the same attribute value does not exist in the database.
    """

    def __init__(self, field_name: str, model_class: ABC, attribute_name: str, error_code: Optional[str] = None, error_message: Optional[str] = None):
        super().__init__(attribute_name)
        self.field_name = field_name
        self.model_class = model_class
        self.attribute_name = attribute_name
        self.error_code = error_code
        self.error_message = error_message

    def validate(self, value):
        """Validates if a record with the same attribute value does not exist in the database."""
        filter_kwargs = {self.attribute_name: value}
        existing_record = self.model_class.objects.filter(**filter_kwargs).first()
        if not existing_record:
            self.add_error(self.error_code, self.error_message)


class RequiredKeysValidator(V2StechValidationError):
    """Validate required keys in data dictionary and raise a validation error if any are missing."""
    
    def __init__(self, required_keys, data, error_code=None, error_message=None):
        """Initialize with required keys, data, error code, and error message (optional)."""
        super().__init__(error_code, error_message)
        self.required_keys = required_keys
        self.data = data
        self.error_code = error_code
        self.error_message = error_message

    def validate(self):
        """Add a validation error if any required keys are missing in the data dictionary."""
        missing_keys = [key for key in self.required_keys if key not in self.data]
        self.error_message = f"Missing required fields: {', '.join(missing_keys)}"
        if missing_keys:
            self.add_error(self.error_code, self.error_message)
            super().validate()

class ModelKwargsExistsError(V2StechValidationError):
    """Error raised when a model instance with specified key-value pairs already exists."""

    def __init__(self, required_keys,model_class: ABC, data, error_code=None, error_message=None,status_code=400):
        """
        Initialize the ModelKwargsExistsError instance.
        """
        super().__init__(error_code, error_message,status_code)
        self.required_keys = required_keys
        self.model_class = model_class
        self.data = data
        self.error_code = error_code
        self.error_message = error_message
        self.status_code = status_code


    def validate(self):
        """Add a validation error if a model instance with specified key-value pairs already exists."""
        filter_keys = {self.required_keys[key]: value for key, value in self.data.items() if key in self.required_keys}
        existing_record = self.model_class.objects.filter(**filter_keys).first()
        if existing_record:
            self.add_error(self.error_code, self.error_message)
            super().validate()


class UniqueDataValidator(V2StechValidationError):
    """Validates the uniqueness of data in a model."""
    def __init__(self,model_class: ABC, kwargs, data, error_code=None, error_message=None,status_code=400):
        super().__init__(error_code, error_message,status_code)
        self.model_class = model_class
        self.kwargs = kwargs
        self.data = data
        self.error_code = error_code
        self.error_message = error_message
        self.status_code = status_code

    def validate(self):
        filter_kwargs = {}
        for key in self.kwargs:
            filter_kwargs[self.kwargs[key]]= self.data.get(key)
        existing_record = self.model_class.objects.filter(**filter_kwargs).first()
        if existing_record:
            self.add_error(self.error_code, self.error_message)
            super().validate()


class FieldRelatedValidator(ValidatorBase):
    """Validate that a field is related to an existing object in the database."""

    def __init__(self, field_name: str, model_class: Model, lookup_field_alias: str, error_code: Optional[str] = None, error_message: Optional[str] = None):
        super().__init__(field_name)
        self.field_name = field_name
        self.model_class = model_class
        self.lookup_field_alias = lookup_field_alias
        self.error_code = error_code
        self.error_message = error_message

    def validate(self, value):
        """Validate that the provided value is related to an existing object in the database."""
        if value:
            filter_kwargs = {self.lookup_field_alias: value}
            existing_object = self.model_class.objects.filter(**filter_kwargs).first()
            if existing_object:
                self.add_error(self.error_code, self.error_message)

from django.urls.resolvers import get_resolver, URLPattern, URLResolver

@dataclass
class URLNameValidator(ValidatorBase):
    """
    Validator for checking if a field contains a valid URL name.
    """
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def validate(self, value):
        # Get all URL names in your Django project
        all_url_names = self.get_all_url_names()
        # Check if the given value is in the list of URL names
        if value not in all_url_names:
            self.add_error(self.error_code, self.error_message)

    def get_all_url_names(self):
        resolver = get_resolver()
        return self.get_url_paths(resolver.url_patterns)

    # def get_url_names(self, url_patterns, namespace=""):
    #     url_names = []
    #     for pattern in url_patterns:
    #         if hasattr(pattern, 'url_patterns'):
    #             url_names.extend(self.get_url_names(pattern.url_patterns, pattern.namespace))
    #         if hasattr(pattern, 'name') and pattern.name:
    #             if namespace:
    #                 url_name = f"{namespace}:{pattern.name}"
    #             else:
    #                 url_name = pattern.name
    #             url_names.append(url_name)
    #     return url_names

    def get_url_paths(self, url_patterns, prefix=""):
        url_paths = []
        for pattern in url_patterns:
            if isinstance(pattern, URLPattern):
                path = prefix + str(pattern.pattern)
                url_paths.append(path)
            elif isinstance(pattern, URLResolver):
                if pattern.pattern:
                    new_prefix = prefix + str(pattern.pattern)
                else:
                    new_prefix = prefix
                url_paths.extend(self.get_url_paths(pattern.url_patterns, new_prefix))
        return url_paths




class UserRegistrationServiceValidator(V2StechValidationError):
    """Error raised when a model instance with specified key-value pairs already exists."""

    def __init__(self, data, error_code=None, error_message=None,status_code=400):
        """
        Initialize the ModelKwargsExistsError instance.
        """
        super().__init__(error_code, error_message,status_code)
        self.data = data
        self.error_code = error_code
        self.error_message = error_message
        self.status_code = status_code


    def validate(self):
        service_array = self.data.get("service")
        # Check if 'user_registration' service is present
        user_registration_present = any(
            service.get("feature_key") == USER_REGISTRATION_FEATURE for service in service_array
        )
        if not user_registration_present:
            self.add_error(self.error_code, self.error_message)
            super().validate()





class ValidationManager:
    """Class for managing data validation methods."""

    def __init__(self, required_keys=None,data=None):
        """Initialize the ValidationManager with a list of required keys (optional).

        Args:
        - required_keys (list): A list of keys that are required for validation.
        """
        self.required_keys = required_keys or []
        self.data = data

    def validate_empty(self, field_name, error_code, error_message):
        """Create and return an EmptyValidator object to validate that a field is not empty."""
        return EmptyValidator(field_name, error_code=error_code, error_message=error_message)

    def validate_string(self, field_name, error_code, error_message):
        """Create and return an StringOnlyValidator object to validate that a field is not empty."""
        return StringOnlyValidator(field_name, error_code=error_code, error_message=error_message)

    def validate_alphanumeric_with_whitespace(self, field_name, error_code, error_message):
        """Create and return an AlphanumericWithWhitespaceValidator object to validate that a field contains only alphanumeric characters and whitespace."""
        return AlphanumericWithWhitespaceValidator(field_name, error_code=error_code, error_message=error_message)

    def validate_alphanumeric_regex(self, field_name, error_code, error_message):
        """Create and return an AlphanumericRegixValidator object to validate that a field contains only alphanumeric characters using regex."""
        return AlphanumericRegixValidator(field_name, error_code=error_code, error_message=error_message)

    def validate_alphabetic_underscore_hiphen(self, field_name, error_code, error_message):
        """Create and return an AlphabeticUnderscoreHyphenValidator object to validate that a field contains only alphabates,underscore,hiphen using regex."""
        return AlphabeticUnderscoreHyphenValidator(field_name, error_code=error_code, error_message=error_message)

    def validate_alphabetic_regex(self, field_name, error_code, error_message):
        """Create and return an AlphabeticRegexValidator object to validate that a field contains only alphabetic characters using regex."""
        return AlphabeticRegexValidator(field_name, error_code=error_code, error_message=error_message)

    def validate_min_max_length(self, field_name, min_length, max_length, error_code, error_message):
        """Create and return a MinMaxLengthValidator object to validate that a field's length is within a specified range."""
        return MinMaxLengthValidator(field_name, min_length=min_length, max_length=max_length, error_code=error_code, error_message=error_message)

    def validate_regex(self, field_name, validation_method, error_code, error_message):
        """Create and return a RegexValidator object to validate a field using a regular expression."""
        return RegexValidator(field_name, validation_method=validation_method, error_code=error_code, error_message=error_message)

    def validate_uppercase_and_underscore_regex(self, field_name, error_code, error_message):
        """Create and return a UppercaseUnderscoreRegexValidator object to validate a field using a regular expression."""
        return UppercaseUnderscoreRegexValidator(field_name, error_code=error_code, error_message=error_message)

    def validate_mobile_number(self, field_name, error_code, error_message):
        """Create and return a MobileNumberValidator object to validate a field using a regular expression."""
        return MobileNumberValidator(field_name, error_code=error_code, error_message=error_message)

    def validate_email(self, field_name, error_code, error_message):
        """Create and return a EmailValidator object to validate a field using a regular expression."""
        return EmailValidator(field_name, error_code=error_code, error_message=error_message)

    def validate_zip_code(self, field_name, error_code, error_message):
        """Create and return a ZipCodeValidator object to validate a field using a regular expression."""
        return ZipCodeValidator(field_name, error_code=error_code, error_message=error_message)

    def validate_model_attribute_exists(self, field_name, model_class, attribute_name, error_code, error_message):
        """Create and return a ModelAttributeExistsValidator object to validate that a model attribute exists in the database."""
        return ModelAttributeExistsValidator(field_name, model_class=model_class, attribute_name=attribute_name, error_code=error_code, error_message=error_message)
    
    def validate_unique_data(self, model_class, kwargs, error_code, error_message,status_code):
        """Create and return a UniqueDataValidator object to validate that a model attribute exists in the database."""
        unique_data_validaor =  UniqueDataValidator(model_class=model_class, kwargs=kwargs, data=self.data ,error_code=error_code, error_message=error_message,status_code=status_code)
        unique_data_validaor.validate()
        
    def validate_model_attribute_not_exists(self, field_name, model_class, attribute_name, error_code, error_message):
        """Create and return a ModelAttributeNotExistsValidator object to validate that a model attribute does not exist in the database."""
        return ModelAttributeNotExistsValidator(field_name, model_class=model_class, attribute_name=attribute_name, error_code=error_code, error_message=error_message)
        
    def validate_model_kwargs_exists(self, filter_kwargs, model_class,data, error_code, error_message):
        """Create and return a ModelKwargsExistsError object to validate that a model kwargs exist in the database."""
        object_exist_with_kwargs = ModelKwargsExistsError(filter_kwargs, model_class=model_class,data=data, error_code=error_code, error_message=error_message)
        object_exist_with_kwargs.validate()
    def validate_field_related(self, field_name, model_class, lookup_field_alias, error_code, error_message):
        """Create and return a FieldRelatedValidator object to validate a field related to another model's field."""
        return FieldRelatedValidator(field_name, model_class=model_class, lookup_field_alias=lookup_field_alias, error_code=error_code, error_message=error_message)

    def validate_url_name(self, field_name, error_code, error_message):
        """Create and return a URLNameValidator object to validate a field."""
        return URLNameValidator(field_name=field_name, error_code=error_code,error_message=error_message)

    def validate_strings_digits(self, field_name, error_code, error_message):
        """Create and return a StringDigitsOnlyValidator object to validate a field."""
        return StringDigitsOnlyValidator(field_name=field_name, error_code=error_code,error_message=error_message)

    def validate_unit(self, field_name, error_code, error_message,valid_units):
        """Create and return a UnitValidator object to validate a field."""
        return UnitValidator(field_name=field_name, error_code=error_code, error_message=error_message, valid_units=valid_units)

    def validate_list_of_dictionary(self, field_name, error_code, error_message):
        """Create and return a ListOfDictionariesValidator object to validate a field."""
        return ListOfDictionariesValidator(field_name=field_name, error_code=error_code, error_message=error_message)

        
    def validate_user_registration_service(self, data, error_code, error_message):
        """Create and return a UserRegistrationServiceValidator object to validate that a model kwargs exist in the database."""
        user_registration_validator = UserRegistrationServiceValidator(data=data, error_code=error_code, error_message=error_message)
        user_registration_validator.validate()

    def check_required_keys(self):
        """Check if required keys are present in the data dictionary and raise a CustomValidationException if they are missing."""
        required_keys_validator = RequiredKeysValidator(self.required_keys, self.data, error_code="E0100")
        required_keys_validator.validate()
