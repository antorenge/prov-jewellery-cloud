"""
Payments app
"""
from djmoney.models.fields import MoneyField
from django.db import models
from apps.shared.helpers import get_unique_code
from apps.shared.audit_log.models.fields import CreatingUserField
from apps.shared.audit_log.models.fields import LastUserField
from apps.purchases.models import PurchaseOrder
from apps.users.models import User
from apps.inventory.models import InventoryItem


class Invoice(models.Model):
    """Invoice model"""
    code = models.CharField(unique=True, primary_key=True,
                            db_index=True, max_length=64, blank=True)
    order = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT)
    due_date = models.DateTimeField()

    def __str__(self):
        return "{}".format(self.code)

    def save(self, * args, ** kwargs):
        if not self.code:
            self.code = get_unique_code()
        super(Invoice, self).save(* args, ** kwargs)

    @property
    def payments(self):
        return self.payment_set.all()

    @property
    def amount_due(self):
        return

    @property
    def amount_paid(self):
        return


class Payment(models.Model):
    """Payment ledger"""
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
    amount = MoneyField(max_digits=10, decimal_places=2,
                        default_currency='EUR', blank=True)
    transaction_id = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.invoice, self.amount)


class OwnershipTransfer(models.Model):
    """Ownership Transfer

    Records transfer of ownership of an inventory item once payment
    transaction is complete
    """
    order = models.OneToOneField(PurchaseOrder, on_delete=models.PROTECT)
    previous_owner = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='previous_owner_%(app_label)s_%(class)s')
    current_owner = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='current_owner_%(app_label)s_%(class)s')

    date_transferred = models.DateTimeField()

    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = CreatingUserField(
        related_name="created_by_%(app_label)s_%(class)s",
        on_delete=models.PROTECT)
    modified_by = LastUserField(
        related_name='modified_by_%(app_label)s_%(class)s',
        on_delete=models.PROTECT)

    def __str__(self):
        return "{} ({})".format(self.current_owner, self.order)

    @property
    def items(self):
        items = InventoryItem.objects.filter(
            delivery__po_product__order=self.order)
        return items
