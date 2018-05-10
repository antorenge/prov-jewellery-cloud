"""
Validation admin views
"""
from django.contrib import admin
from apps.inventory.models import InventoryItem
from .models import Validation, WorkInProgress


class ValidationAdmin(admin.ModelAdmin):
    """Production validation admin view"""
    list_display = ('item', 'is_approved', 'date_validated',
                    'validated_by', 'stage')

    fieldsets = (
        (None, {
            'fields': ('item', 'is_approved', 'stage')
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.validated_by = request.user
        super(ValidationAdmin, self).save_model(request, obj, form, change)


class WorkInProgressAdmin(admin.ModelAdmin):
    list_display = ('product', 'workshop', 'quantity_received',
                    'date_received', 'quantity_delivered', 'date_delivered',
                    'process')

    fieldsets = (
        (None, {
            'fields': ('workshop', 'process', 'product')
        }),
        ('Receive', {
            'classes': ('collapse',),
            'fields': ('received_items', 'quantity_received', 'date_received',
                       'received_from'),
        }),
        ('Deliver', {
            'classes': ('collapse',),
            'fields': ('delivered_items', 'quantity_delivered',
                       'date_delivered', 'delivered_to'),
        }),
    )


admin.site.register(WorkInProgress, WorkInProgressAdmin)
admin.site.register(Validation, ValidationAdmin)
