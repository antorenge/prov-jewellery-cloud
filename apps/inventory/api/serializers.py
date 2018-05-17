"""
Inventory serializers
"""
from rest_framework import serializers
from apps.products.api.serializers import ProductDesignSerializer
from apps.purchases.api.serializers import PurchaseOrderDelivery
from apps.validations.api.serializers import WorkInProgressSerializer
from ..models import InventoryItem


class InventoryItemSerializer(serializers.ModelSerializer):
    """Serializer for inventory items"""

    product = ProductDesignSerializer()
    delivery = PurchaseOrderDelivery()
    wip = WorkInProgressSerializer()

    class Meta:
        model = InventoryItem
        fields = ('serial_no', 'product', 'delivery', 'wip',)
