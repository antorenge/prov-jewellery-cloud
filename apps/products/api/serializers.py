"""
Product Design API
"""
from rest_framework import serializers
from apps.users.api.serializers import UserSerializer
from ..models import (Image, Drawing, ProductDesign, Material, BillOfMaterial,
                      Component, Technique, Dimension)


class DimensionSerializer(serializers.ModelSerializer):
    """Serializer for dimensions"""

    class Meta:
        model = Dimension
        fields = ('attribute', 'measurement')


class ImageSerializer(serializers.ModelSerializer):
    """Serializer for images"""

    class Meta:
        model = Image
        fields = ('file', 'label')


class DrawingSerializer(serializers.ModelSerializer):
    """Serializer for drawings"""

    class Meta:
        model = Drawing
        fields = ('file', 'label')


class TechniqueSerializer(serializers.ModelSerializer):
    """Serializer for Technique model"""

    class Meta:
        model = Technique
        fields = ('name',)


class MaterialSerializer(serializers.ModelSerializer):
    """Serializer for Material model"""
    techniques = serializers.StringRelatedField(
        source='materialtechnique_set', many=True)

    class Meta:
        model = Material
        fields = ('name', 'units_of_measurement', 'techniques')


class BillOfMaterialSerializer(serializers.ModelSerializer):
    """Serializer for bill of materials"""

    material = MaterialSerializer()

    class Meta:
        model = BillOfMaterial
        fields = ('material', 'quantity')


class MiniProductDesignSerializer(serializers.ModelSerializer):
    """Mini serializer for product design model"""

    dimensions = DimensionSerializer(many=True)
    images = ImageSerializer(many=True)
    drawings = DrawingSerializer(many=True)
    bill_of_materials = BillOfMaterialSerializer(
        source='billofmaterial_set', many=True)
    designers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ProductDesign
        fields = ('sku', 'name', 'collection', 'category', 'year', 'variance',
                  'color', 'size', 'shape', 'dimensions', 'images', 'drawings',
                  'bill_of_materials', 'designers')


class ComponentSerializer(serializers.ModelSerializer):
    """Serializer for Component model"""
    child = MiniProductDesignSerializer()

    class Meta:
        model = Component
        fields = ('child', 'quantity')


class ProductDesignSerializer(serializers.ModelSerializer):
    """Serializer for product design model"""

    dimensions = DimensionSerializer(many=True)
    images = ImageSerializer(many=True)
    drawings = DrawingSerializer(many=True)
    bill_of_materials = BillOfMaterialSerializer(
        source='billofmaterial_set', many=True)
    components = ComponentSerializer(source='parent_product', many=True)
    designers = UserSerializer(many=True, read_only=True)
    created_by = UserSerializer()
    modified_by = UserSerializer()

    class Meta:
        model = ProductDesign
        fields = ('sku', 'name', 'collection', 'category', 'year', 'variance',
                  'color', 'size', 'shape', 'dimensions', 'images', 'drawings',
                  'bill_of_materials', 'designers', 'components',
                  'date_created', 'date_modified', 'created_by', 'modified_by')

    def create(self, validated_data):
        product_design = ProductDesign.objects.create(**validated_data)
        # Create images
        images_data = validated_data.pop('images')
        for image_data in images_data:
            Image.objects.create(product=product_design, **image_data)

        # Create drawings
        drawings_data = validated_data.pop('drawings')
        for drawing_data in drawings_data:
            Drawing.objects.create(product=product_design, **drawing_data)

        # Create bill of materials
        bill_of_materials_data = validated_data.pop('bill_of_materials')
        for bill_of_material_data in bill_of_materials_data:
            BillOfMaterial.objects.create(
                product=product_design, **bill_of_material_data)

        return product_design


class ValidateSerializer(serializers.Serializer):
    """Validate JSON web tokens serializer"""
    sku = serializers.CharField(max_length=200)
    token = serializers.CharField()
