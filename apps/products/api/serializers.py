"""
Product Design API
"""
from rest_framework import serializers
from apps.users.api.serializers import UserSerializer
from ..models import (Image, Drawing, ProductDesign, Material, BillOfMaterial,
                      Component)


class ImageSerializer(serializers.ModelSerializer):
    """Serializer for images"""
    class Meta:
        model = Image
        fields = ('id', 'file', 'label')


class DrawingSerializer(serializers.ModelSerializer):
    """Serializer for drawings"""
    class Meta:
        model = Drawing
        fields = ('id', 'file', 'label')


class MaterialSerializer(serializers.ModelSerializer):
    """Serializer for Material model"""

    class Meta:
        model = Material
        fields = ('name', 'units_of_measurement')


class BillOfMaterialSerializer(serializers.ModelSerializer):
    """Serializer for bill of materials"""

    material = MaterialSerializer()

    class Meta:
        model = BillOfMaterial
        fields = ('material', 'quantity')


class ProductDesignSerializer(serializers.ModelSerializer):
    """Serializer for product design model"""

    images = ImageSerializer(many=True, read_only=True)
    drawings = DrawingSerializer(many=True, read_only=True)
    bill_of_materials = BillOfMaterialSerializer(
        source='billofmaterial_set', many=True, read_only=True)
    designers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ProductDesign
        fields = ('sku', 'name', 'collection', 'category', 'year', 'variance',
                  'color', 'size', 'shape', 'images', 'drawings',
                  'bill_of_materials', 'designers', 'date_created',
                  'date_modified', 'created_by', 'modified_by')


class ComponentSerializer(serializers.ModelSerializer):
    """Serializer for Component model"""
    parent = ProductDesignSerializer()
    child = ProductDesignSerializer()

    class Meta:
        model = Component
        fields = "__all__"
