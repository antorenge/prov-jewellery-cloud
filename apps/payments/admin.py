"""
Payments admin views
"""
from django.contrib import admin
from .models import Invoice, Payment, OwnershipTransfer


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('code', 'order', 'amount', 'amount_due', 'due_date')

    fieldsets = (
        (None, {
            'fields': ('order', 'amount', 'due_date')
        }),
    )


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount', 'transaction_id')


class OwnershipTransferAdmin(admin.ModelAdmin):
    list_display = ('order', 'previous_owner', 'current_owner',
                    'date_transferred')


admin.site.register(OwnershipTransfer, OwnershipTransferAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Invoice, InvoiceAdmin)
