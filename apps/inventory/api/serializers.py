"""
Inventory serializers
"""
from rest_framework import serializers
from ..models import InventoryItem


class InventoryItemSerializer(serializers.ModelSerializer):
    """Serializer for inventory items"""

    class Meta:
        model = InventoryItem
        fields = ('serial_no',)
