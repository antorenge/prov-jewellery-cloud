from django.db import models
from apps.products.models import Product
from apps.purchases.models import PurchaseOrderDelivery


class InventoryItem(models.Model):
    """Uniquely tracks each item delivered by an artisan"""
    serial_no = models.CharField(unique=True, primary_key=True,
                                 db_index=True, max_length=128, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    delivery = models.ForeignKey(PurchaseOrderDelivery,
                                 on_delete=models.PROTECT)
    wip = models.ForeignKey('validations.WorkInProgress',
                            on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.product, self.serial_no)
