"""
WIP serializer
"""
from rest_framework import serializers
from apps.users.api.serializers import UserSerializer
from apps.products.api.serializers import ProductDesignSerializer
from apps.purchases.api.serializers import WorkshopSerializer
from ..models import WorkInProgress


class WorkInProgressSerializer(serializers.ModelSerializer):
    """Serializer for wip's"""

    product = ProductDesignSerializer()
    workshop = WorkshopSerializer()
    received_from = UserSerializer()
    delivered_to = UserSerializer()
    created_by = UserSerializer()
    modified_by = UserSerializer()

    class Meta:
        model = WorkInProgress
        fields = ('id', 'product', 'workshop', 'process', 'received_items',
                  'quantity_received', 'date_received', 'received_from',
                  'delivered_items', 'quantity_delivered', 'date_delivered',
                  'delivered_to', 'date_created', 'date_modified',
                  'created_by', 'modified_by')
