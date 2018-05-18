"""
Payments API
"""
from rest_framework import serializers
from apps.users.api.serializers import UserSerializer
from apps.purchases.api.serializers import PurchaseOrderSerializer
from apps.inventory.api.serializers import InventoryItemSerializer
from ..models import OwnershipTransfer


class OwnershipTransferSerializer(serializers.ModelSerializer):
    """Serializer for ownership transfers"""

    order = PurchaseOrderSerializer()
    previous_owner = UserSerializer()
    current_owner = UserSerializer()
    created_by = UserSerializer()
    modified_by = UserSerializer()
    items = InventoryItemSerializer()

    class Meta:
        model = OwnershipTransfer
        fields = ('order', 'previous_owner', 'current_owner', 'items',
                  'date_transferred', 'date_created', 'date_modified',
                  'created_by', 'modified_by')
