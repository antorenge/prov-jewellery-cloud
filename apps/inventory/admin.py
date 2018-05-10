"""
Inventory admin views
"""
from django.contrib import admin
from .models import InventoryItem


class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('serial_no', 'product', 'delivery',)


admin.site.register(InventoryItem, InventoryItemAdmin)
