"""
Purchases models
"""
from djmoney.models.fields import MoneyField
from django.db import models
from django.apps import apps
from django.core.validators import MinValueValidator
from apps.shared.audit_log.models.fields import CreatingUserField
from apps.shared.audit_log.models.fields import LastUserField
from apps.shared.helpers import get_unique_code
from apps.products.models import Product, Material
from apps.users.models import User


class PurchaseOrder(models.Model):
    """Purchase order model"""
    code = models.CharField(unique=True, primary_key=True,
                            db_index=True, max_length=64, blank=True)
    name = models.CharField(max_length=160, blank=True)
    workshop = models.ForeignKey('Workshop', on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, through='PurchaseOrderProduct')
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    artisans = models.ManyToManyField(User)

    def __str__(self):
        return "{} ({})".format(self.name, self.code)

    def save(self, * args, ** kwargs):
        if not self.code:
            self.code = get_unique_code()
        super(PurchaseOrder, self).save(* args, ** kwargs)


class PurchaseOrderProduct(models.Model):
    """Model for products ordered in a purchase order"""
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_ordered = models.FloatField(
        validators=[MinValueValidator(0.00), ], default=0.00)
    unit_price = MoneyField(max_digits=10, decimal_places=2,
                            default_currency='EUR', blank=True)

    def __str__(self):
        return "{} ({})".format(self.product, self.quantity_ordered)


class PurchaseOrderDelivery(models.Model):
    """Tracks deliveries made for a product"""
    po_product = models.ForeignKey(
        PurchaseOrderProduct, on_delete=models.PROTECT)
    quantity_delivered = models.FloatField(
        validators=[MinValueValidator(0.00), ], default=0.00)
    quantity_received = models.FloatField(
        validators=[MinValueValidator(0.00), ], default=0.00)
    date_delivered = models.DateTimeField()
    date_received = models.DateTimeField()

    def __str__(self):
        return "{} ({})".format(self.product, self.quantity_delivered)


class Workshop(models.Model):
    """Workshop model"""
    name = models.CharField(max_length=160, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Location(models.Model):
    """Geo location address"""
    name = models.CharField(max_length=160, blank=True)
    latitude = models.FloatField(
        validators=[MinValueValidator(0.00), ], default=0.00)
    longitude = models.FloatField(
        validators=[MinValueValidator(0.00), ], default=0.00)

    def __str__(self):
        return "{}".format(self.name)


class ArtisanProduction(models.Model):
    """Artisan production model"""
    po_product = models.ForeignKey(
        PurchaseOrderProduct, on_delete=models.PROTECT)
    quantity_produced = models.FloatField(
        validators=[MinValueValidator(0.00), ], default=0.00)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = CreatingUserField(
        related_name="created_by_%(app_label)s_%(class)s",
        on_delete=models.PROTECT)
    modified_by = LastUserField(
        related_name='modified_by_%(app_label)s_%(class)s',
        on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    def __str__(self):
        return "{} ({})".format(self.po_product, self.quantity_produced)

    @property
    def items(self):
        """Return list of items at a granular level delivered by an artisan"""
        inventory = apps.get_model('inventory', 'InventoryItem')
        return inventory.objects.filter(production=self)


class Supplier(models.Model):
    """Source of materials used in artisan production"""
    production = models.ForeignKey(ArtisanProduction, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    name = models.CharField(max_length=160, blank=True)
    address = models.TextField(blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.name)
