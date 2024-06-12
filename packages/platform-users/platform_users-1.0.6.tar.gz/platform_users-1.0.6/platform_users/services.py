#Python Imports

#Django Imports

#Third-Party Imports
from rest_framework import status

#Project-Specific Imports
from common_utils.base_service import BaseService
from common_utils.exceptions import CustomValidationException
from common_utils.pagination import GenericPaginator
from common_utils.utils import AttributeMapper


#Relative Import
from .models import Users
from .serializers import UsersSerializer,UsersListSerializer
from .errors import UsersErrorMessages


class UsersService(BaseService):
    """Users-related operations."""

    object_name = 'Users'

    @staticmethod
    def get_user_object(pk=None,is_deleted=None,**kwargs):
        user = UsersService.get_object_by_id(Users,pk=pk,is_deleted=is_deleted,**kwargs)
        if user:
            return user
        errors = UsersErrorMessages().get_user_not_exists_message()
        raise CustomValidationException(errors=errors, status_code=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_user_object_by_attr(attribute_name=None, attribute_value=None, is_deleted=False, **kwargs):
        """Get a user object by its attribute and value and return it if found, or raise a 404 error if not found."""
        if attribute_name is None:
            attribute_name = 'username'
        attribute_name = Users._meta.get_field(attribute_name).verbose_name
        user = UsersService.get_object_by_attr(Users, attribute_name=attribute_name, attribute_value=attribute_value, is_deleted=is_deleted, **kwargs)
        if user:
            return user
        errors = UsersErrorMessages().get_user_not_exists_message()
        raise CustomValidationException(errors=errors, status_code=status.HTTP_404_NOT_FOUND)


    @staticmethod
    def list_users(**kwargs):
        """Retrieve a paginated list of users."""
        page_number = kwargs.pop('page_number')
        page_size = kwargs.pop('page_size')
        queryset = UsersService.get_all(Users, ordering='-date_joined', **kwargs)
        data = GenericPaginator.paginate(
            queryset, UsersListSerializer, page_number, page_size)
        return data

    @staticmethod
    def create_user(data):
        """Create a new user."""
        return BaseService.create(UsersSerializer, Users, data)


    @staticmethod
    def get_user_details(username):
        """Retrieve details of a specific user by username."""
        user = UsersService.get_user_object_by_attr(attribute_value=username)
        return UsersService.list_details(user, UsersSerializer)

    @staticmethod
    def update_user(username, data, partial=False):
        """Update a specific user by username."""
        user = UsersService.get_user_object_by_attr(attribute_value=username)
        return UsersService.update(user, UsersSerializer, data=data,  partial=partial)


    @staticmethod
    def is_default_user_exists():
        """Check if at least one user has is_default set to True. Returns True if the condition is met, False otherwise."""
        kwargs = AttributeMapper(is_default=True).to_dict()
        default_user_exists = UsersService.get_user_by_kwargs(**kwargs)
        return default_user_exists


    @staticmethod
    def get_user_by_kwargs(**kwargs):
        """get user by kwargs"""
        
        user = UsersService.get_object_by_id(Users,pk=None,is_deleted=False,**kwargs)
        if user:
            return user
        return None
