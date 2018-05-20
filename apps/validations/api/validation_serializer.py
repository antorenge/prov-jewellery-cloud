"""
Validations serializer
"""
from rest_framework import serializers
from apps.users.api.serializers import UserSerializer
from apps.inventory.api.serializers import InventoryItemSerializer
from ..models import Validation


class ValidationSerializer(serializers.ModelSerializer):
    """Serializer for validations"""

    item = InventoryItemSerializer()
    validated_by = UserSerializer()

    class Meta:
        model = Validation
        fields = ('id', 'item', 'is_approved', 'date_validated',
                  'validated_by', 'stage')
