"""
Purchases API
"""
from rest_framework import serializers
from apps.users.api.serializers import UserSerializer
from apps.products.api.serializers import (MaterialSerializer,
                                           ProductDesignSerializer)
from ..models import (ArtisanProduction, Supplier, Location,
                      PurchaseOrderProduct, PurchaseOrderDelivery)


class PurchaseOrderProductSerializer(serializers.ModelSerializer):
    """Serializer for purchase order products"""

    product = ProductDesignSerializer()

    class Meta:
        model = PurchaseOrderProduct
        fields = ('product', 'quantity_ordered', 'unit_price')


class PurchaseOrderDeliverySerializer(serializers.ModelSerializer):
    """Serializer for deliveries"""

    po_product = PurchaseOrderProductSerializer()
    delivered_by = UserSerializer()
    received_by = UserSerializer()

    class Meta:
        model = PurchaseOrderDelivery
        fields = ('po_product', 'quantity_delivered', 'quantity_received',
                  'date_delivered', 'date_received', 'delivered_by',
                  'received_by')


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for locations"""

    class Meta:
        model = Location
        fields = ('name', 'longitude', 'latitude')


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for suppliers"""

    material = MaterialSerializer()
    location = LocationSerializer()

    class Meta:
        model = Supplier
        fields = ('material', 'name', 'address', 'location')


class ArtisanProductionSerializer(serializers.ModelSerializer):
    """Serializer for artisan productions"""

    po_product = PurchaseOrderProductSerializer()
    suppliers = SupplierSerializer(source='supplier_set', many=True)
    location = LocationSerializer()
    created_by = UserSerializer()
    modified_by = UserSerializer()

    class Meta:
        model = ArtisanProduction
        fields = ('po_product', 'quantity_produced', 'date_created',
                  'date_modified', 'created_by', 'modified_by', 'location',
                  'suppliers')
