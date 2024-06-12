#Python Imports

#Django Imports
from django.utils import timezone

#Third-Party Imports

#Project-Specific Imports

#Relative Import



class DateTimeUtil:
    @staticmethod
    def get_django_current_datetime():
        """
        Get the current datetime using Django's timezone.

        Returns:
            datetime: The current datetime in the UTC timezone.
        """
        return timezone.now()
