from django.db import models
from apps.products.models import Product
from apps.purchases.models import ArtisanProduction, PurchaseOrderDelivery


class InventoryItem(models.Model):
    """Uniquely tracks each item delivered by an artisan"""
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    production = models.ForeignKey(ArtisanProduction, on_delete=models.PROTECT)
    delivery = models.ForeignKey(
        PurchaseOrderDelivery, on_delete=models.PROTECT)

    def __str__(self):
        return "{} ({})".format(self.product, self.pk)
