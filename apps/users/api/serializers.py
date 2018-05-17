"""
Users API views
"""
from rest_framework import serializers, exceptions
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'email', 'phone',
                  'picture', 'is_staff', 'is_active', 'date_joined')
