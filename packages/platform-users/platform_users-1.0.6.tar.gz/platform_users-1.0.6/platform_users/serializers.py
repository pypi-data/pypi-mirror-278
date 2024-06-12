#Python Imports

#Django Imports
from django.contrib.auth.hashers import make_password

#Third-Party Imports
from rest_framework import serializers


#Project-Specific Imports

#Relative Import
from .models import Users  

class UsersSerializer(serializers.ModelSerializer):
    """Serializer for the Users model, including password hashing during creation and update."""
    
    class Meta:
        model = Users
        fields = '__all__'
        read_only_fields = ['is_default']


    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance, validated_data):

        # Hash the password if provided
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data.get('password'))
        
        return super().update(instance, validated_data)
    
    
class UsersListSerializer(serializers.ModelSerializer):
    """Serializer for the List Users."""
    
    class Meta:
        model = Users
        exclude = ['password']

