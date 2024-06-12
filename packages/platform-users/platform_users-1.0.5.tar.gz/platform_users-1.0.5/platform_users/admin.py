#Python Imports

#Django Imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#Third-Party Imports

#Project-Specific Imports
from platform_users.models import Users

#Relative Import



class CustomUserAdmin(UserAdmin):
    model = Users
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_default', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'mobile_number')
    list_filter = ('is_active', 'is_default', 'date_joined')  # Add the fields you want to filter by
    filter_horizontal = ()  # Remove references to 'groups' and 'user_permissions'

# Register your custom admin for the Users model
admin.site.register(Users, CustomUserAdmin)
