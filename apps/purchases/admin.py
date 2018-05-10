"""
Purchases admin views
"""
from django.contrib import admin
from .models import (PurchaseOrder, PurchaseOrderProduct,
                     PurchaseOrderDelivery, Workshop, Location,
                     ArtisanProduction, Supplier)


class PurchaseOrderProductInline(admin.StackedInline):
    """Inline view for PO products"""

    model = PurchaseOrderProduct
    fk_name = 'order'
    extra = 1
    verbose_name_plural = ''


class PurchaseOrderAdmin(admin.ModelAdmin):
    """Purchase order admin view"""
    list_display = ('code', 'name', 'workshop', 'due_date')

    fieldsets = (
        (None, {
            'fields': ('name', 'workshop', 'due_date')
        }),
    )

    inlines = (PurchaseOrderProductInline, )


class PurchaseOrderProductAdmin(admin.ModelAdmin):
    """Products ordered admin view"""
    list_display = ('product', 'order', 'quantity_ordered', 'unit_price')


class PurchaseOrderDeliveryAdmin(admin.ModelAdmin):
    """Deliveries made to a product admin view"""
    list_display = ('po_product', 'quantity_delivered', 'date_delivered',
                    'quantity_received', 'date_received')

    fieldsets = (
        (None, {
            'fields': ('po_product', 'quantity_delivered', 'date_delivered',
                       'delivered_by')
        }),
        ('Receive delivery', {
            'classes': ('collapse',),
            'fields': ('quantity_received', 'date_received', 'received_by'),
        }),
    )


class WorkshopAdmin(admin.ModelAdmin):
    """Workshop admin view"""
    list_display = ('name', 'address')


class LocationAdmin(admin.ModelAdmin):
    """Geo locations admin view"""
    list_display = ('name', 'latitude', 'longitude')


class SupplierInline(admin.StackedInline):
    """Inline view for suppliers"""

    model = Supplier
    fk_name = 'production'
    extra = 1
    verbose_name_plural = ''


class ArtisanProductionAdmin(admin.ModelAdmin):
    """Artisan production admin view"""
    list_display = ('po_product', 'quantity_produced', 'created_by',
                    'date_created', 'location')

    inlines = (SupplierInline,)


admin.site.register(ArtisanProduction, ArtisanProductionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(PurchaseOrderDelivery, PurchaseOrderDeliveryAdmin)
admin.site.register(PurchaseOrderProduct, PurchaseOrderProductAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
