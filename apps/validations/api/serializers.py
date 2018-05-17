"""
Validations API
"""
from rest_framework import serializers
from apps.users.api.serializers import UserSerializer
from apps.products.api.serializers import MaterialSerializer
from ..models import Validation, WorkInProgress


class ValidationSerializer(serializers.ModelSerializer):
    """Serializer for validations"""

    validated_by = UserSerializer()

    class Meta:
        model = Validation
        fields = ('item', 'is_approved', 'date_validated', 'validated_by',
                  'stage')


class WorkInProgressSerializer(serializers.ModelSerializer):
    """Serializer for wip's"""

    received_from = UserSerializer()
    delivered_to = UserSerializer()
    created_by = UserSerializer()
    modified_by = UserSerializer()

    class Meta:
        model = WorkInProgress
        fields = ('product', 'workshop', 'process', 'received_items',
                  'quantity_received', 'date_received', 'received_from',
                  'delivered_items', 'quantity_delivered', 'date_delivered',
                  'delivered_to', 'date_created', 'date_modified',
                  'created_by', 'modified_by')
