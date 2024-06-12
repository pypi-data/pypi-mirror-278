
#Python Imports

#Django Imports

#Third-Party Imports

#Project-Specific Imports

#Relative Import
from .models import Users

class UserManager:
    @staticmethod
    def is_default_user_exists():
        """
        Check if there is only one user with is_default set to True.
        Return True if the condition is met, False otherwise.
        """
        default_user_exists = Users.objects.filter(is_default=True).exists()

        return default_user_exists


    @staticmethod
    def ensure_one_default_user(user: Users):
        """
        Ensure that there is at least one user with is_default set to True.
        If not, raise an error and suggest creating another user as the default user.
        """
        existing_default_user = Users.objects.filter(is_default=True).exclude(pk=user.pk).first()
        return existing_default_user
