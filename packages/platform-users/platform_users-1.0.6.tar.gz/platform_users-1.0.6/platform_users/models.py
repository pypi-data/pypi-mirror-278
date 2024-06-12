"""
This module allows importing AbstractBaseUser even when django.contrib.auth is
not in INSTALLED_APPS.
"""

# Python Imports
import unicodedata
import warnings

# Django Imports
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
    check_password,
    is_password_usable,
    make_password,
)
from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django.core import validators
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.itercompat import is_iterable
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string, salted_hmac
from django.utils.translation import gettext_lazy as _


# Third-Party Imports

# Project-Specific Imports

# Relative Import


class BaseUserManager(models.Manager):
    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()
        return email

    def make_random_password(
        self,
        length=10,
        allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789",
    ):
        """
        Generate a random password with the given length and given
        allowed_chars. The default value of allowed_chars does not have "I" or
        "O" or letters and digits that look similar -- just to avoid confusion.
        """
        warnings.warn(
            "BaseUserManager.make_random_password() is deprecated.",
            # category=RemovedInDjango51Warning,
            stacklevel=2,
        )
        return get_random_string(length, allowed_chars)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class AbstractBaseUser(models.Model):
    password = models.CharField(_("password"), max_length=128)

    is_active = True

    REQUIRED_FIELDS = []

    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_username()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def natural_key(self):
        return (self.get_username(),)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        return self._get_session_auth_hash()

    def get_session_auth_fallback_hash(self):
        for fallback_secret in settings.SECRET_KEY_FALLBACKS:
            yield self._get_session_auth_hash(secret=fallback_secret)

    def _get_session_auth_hash(self, secret=None):
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(
            key_salt,
            self.password,
            secret=secret,
            algorithm="sha256",
        ).hexdigest()

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return "email"

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )


class CustomUserManager(BaseUserManager):
    """Custom manager for creating and managing users."""

    def create_user(self, username, email, password=None, **extra_fields):
        """Create a regular user."""
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create a superuser."""
        return self.create_user(username, email, password, **extra_fields)


class Users(AbstractBaseUser):
    """Custom user model."""

    id = models.AutoField(primary_key=True, db_column="ID")
    username = models.CharField(
        max_length=255, unique=True, db_index=True, db_column="USERNAME"
    )
    email = models.EmailField(unique=True, db_index=True, db_column="EMAIL")
    first_name = models.CharField(
        max_length=255, blank=True, null=True, db_column="FIRST_NAME"
    )
    last_name = models.CharField(
        max_length=255, blank=True, null=True, db_column="LAST_NAME"
    )
    mobile_number = models.CharField(
        max_length=15,
        unique=True,
        db_index=True,
        validators=[
            validators.RegexValidator(
                regex=r"^\d{10,15}$",  # Define your regex pattern for validation
                message="Mobile number must be 10 to 15 digits long and contain only digits.",
                code="invalid_mobile_number",
            )
        ],
        blank=True,
        null=True,
        db_column="MOBILE_NUMBER",
    )
    is_active = models.BooleanField(default=True, db_column="IS_ACTIVE")
    is_default = models.BooleanField(default=False, db_column="IS_DEFAULT")
    is_deleted = models.BooleanField(default=False, db_column="IS_DELETED")
    date_joined = models.DateTimeField(default=timezone.now, db_column="DATE_JOINED")
    password = models.CharField(max_length=128, db_column="PASSWORD")
    last_login = models.DateTimeField(default=timezone.now, db_column="LAST_LOGIN")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = "users"

    def has_module_perms(self, app_label):
        # You can customize the logic for checking module permissions here
        # For simplicity, we return True for all users
        return True

    def get_user_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has directly.
        Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, "user")

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, "group")

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "all")

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        print(obj)
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        if not is_iterable(perm_list) or isinstance(perm_list, str):
            raise ValueError("perm_list must be an iterable of permissions.")
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    @property
    def is_staff(self):
        # Customize the logic to determine staff status based on your requirements
        return self.is_default

    @property
    def is_superuser(self):
        # Customize the logic to determine staff status based on your requirements
        return self.is_default

    def set_default_user(self, is_default=True):
        """
        Set or unset the user as the default user.

        Args:
            is_default (bool): If True, set the user as the default user. If False, unset the user as the default user.
        """
        # Ensure there is only one default user if setting is_default to True
        if is_default:
            if Users.objects.filter(is_default=True).exclude(pk=self.pk).exists():
                raise ValidationError(
                    "There is already a default user. Cannot set another user as default."
                )

        self.is_default = is_default
        self.save()


# # A few helper functions for common logic between User and AnonymousUser.
# def _user_get_permissions(user, obj, from_name):
#     return user.is_default

# def _user_has_perm(user, perm, obj):
#     """
#     A backend can raise `PermissionDenied` to short-circuit permission checking.
#     """
#     return user.is_default


# def _user_has_module_perms(user, app_label):
#     """
#     A backend can raise `PermissionDenied` to short-circuit permission checking.
#     """
#     return user.is_default


# A few helper functions for common logic between User and AnonymousUser.
def _user_get_permissions(user, obj, from_name):
    permissions = set()
    name = "get_%s_permissions" % from_name
    for backend in auth.get_backends():
        if hasattr(backend, name):
            permissions.update(getattr(backend, name)(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, "has_perm"):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def _user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, "has_module_perms"):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False
