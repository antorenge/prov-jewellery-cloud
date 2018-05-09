"""
Model admin views for Product
"""
from django.contrib import admin
from django.template.loader import render_to_string
from .models import (Product, Component, Image, Drawing, Dimension,
                     Material, Technique, BillOfMaterial, MaterialTechnique)


class DimensionInline(admin.StackedInline):
    """Inline view for dimensions"""

    model = Dimension
    fk_name = 'product'
    extra = 1
    verbose_name_plural = ''


class DrawingInline(admin.StackedInline):
    """Inline view for drawings"""

    model = Drawing
    fk_name = 'product'
    extra = 1
    verbose_name_plural = ''


class ImageInline(admin.StackedInline):
    """Inline view for images"""

    model = Image
    fk_name = 'product'
    extra = 1
    verbose_name_plural = ''


class ComponentInline(admin.StackedInline):
    """Inline view for components"""

    model = Component
    fk_name = 'parent'
    extra = 1
    verbose_name_plural = ''


class BillOfMaterialInline(admin.StackedInline):
    """Inline view for bill of materials"""

    model = BillOfMaterial
    fk_name = 'product'
    extra = 1
    verbose_name_plural = ''


class ProductAdmin(admin.ModelAdmin):
    """Admin view for products"""
    list_display = ('sku', 'name', 'product_image', 'collection', 'category',
                    'year', 'color', 'size')

    fieldsets = (
        (None, {
            'fields': ('name', 'collection', 'category', 'variance', 'year',
                       'color', 'size', 'shape')
        }),
    )

    inlines = (
        ImageInline,
        DrawingInline,
        DimensionInline,
        BillOfMaterialInline,
        ComponentInline,
    )

    def product_image(self, obj):
        """Return the image of the product"""
        if obj.default_image:
            return render_to_string('product_image.html', {
                'image': obj.default_image.file,
            })
    product_image.short_description = 'Image'


class MaterialTechniqueInline(admin.StackedInline):
    """Inline view for material techniques"""

    model = MaterialTechnique
    fk_name = 'material'
    extra = 1
    verbose_name_plural = ''


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'units_of_measurement')

    fieldsets = (
        (None, {
            'fields': ('name', 'units_of_measurement')
        }),
    )

    inlines = (
        MaterialTechniqueInline,
    )


class TechniqueAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Technique, TechniqueAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Product, ProductAdmin)
