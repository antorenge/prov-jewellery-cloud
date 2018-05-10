"""
Validation admin views
"""
from django.contrib import admin
from .models import Validation


class ValidationAdmin(admin.ModelAdmin):
    """Production validation admin view"""
    list_display = ('item', 'is_approved', 'date_validated', 'delivered_by')


admin.site.register(Validation, ValidationAdmin)
