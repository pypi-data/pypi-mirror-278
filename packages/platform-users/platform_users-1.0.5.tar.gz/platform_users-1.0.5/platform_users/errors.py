#Python Imports
from dataclasses import dataclass, field

#Django Imports

#Third-Party Imports

#Project-Specific Imports
from common_utils.errors import V2stechErrorMessageHandler,get_error_message

#Relative Import

class UsersErrorMessageCodes:
    """
    Class that defines error codes related to users.
    """

    USER_NOT_EXISTS = "E0642"
    CANNOT_DELETE_DEFAULT_USER = "E0019"
    CANNOT_DELETE_USER_ASSIGN_TO_ROLE = "E0020"
    IS_DEFAULT_USER_ALREADY_PRESENT= "E0021"

class UsersErrorMessages(V2stechErrorMessageHandler):
    """
    Class for generating error messages related to users.
    """

    def get_user_not_exists_message(self):
        self.add_message(UsersErrorMessageCodes.USER_NOT_EXISTS, get_error_message(UsersErrorMessageCodes.USER_NOT_EXISTS))
        return self.get_messages()

    def get_cannot_delete_user_assigned_to_role_message(self):
        self.add_message(UsersErrorMessageCodes.CANNOT_DELETE_USER_ASSIGN_TO_ROLE, get_error_message(UsersErrorMessageCodes.CANNOT_DELETE_USER_ASSIGN_TO_ROLE))
        return self.get_messages()

    def get_cannot_delete_default_user_message(self):
        self.add_message(UsersErrorMessageCodes.CANNOT_DELETE_DEFAULT_USER, get_error_message(UsersErrorMessageCodes.CANNOT_DELETE_DEFAULT_USER))
        return self.get_messages()

    def get_default_user_already_present_message(self):
        self.add_message(UsersErrorMessageCodes.IS_DEFAULT_USER_ALREADY_PRESENT, get_error_message(UsersErrorMessageCodes.IS_DEFAULT_USER_ALREADY_PRESENT))
        return self.get_messages()

class TenantAdminErrorMessageCodes:
    """
    Class that defines error codes related to tenant admin.
    """

    FAILED_TO_CREATE_TENANT_ADMIN = "E0642"

class TenantAdminErrorMessages(V2stechErrorMessageHandler):
    """
    Class for generating error messages related to tenant admin.
    """

    def get_failed_to_create_tenant_admin_message(self):
        self.add_message(TenantAdminErrorMessageCodes.FAILED_TO_CREATE_TENANT_ADMIN, get_error_message(TenantAdminErrorMessageCodes.FAILED_TO_CREATE_TENANT_ADMIN))
        return self.get_messages()
