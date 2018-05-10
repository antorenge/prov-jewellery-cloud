"""
Purchases models
"""
from djmoney.models.fields import MoneyField
from moneyed import Money, EUR
from django.db import models
from django.apps import apps
from django.db.models import Q, Sum, F
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
    due_date = models.DateTimeField()
    artisans = models.ManyToManyField(User)

    def __str__(self):
        return "{} ({})".format(self.name, self.code)

    def save(self, * args, ** kwargs):
        if not self.code:
            self.code = get_unique_code()
        super(PurchaseOrder, self).save(* args, ** kwargs)

    def po_products(self):
        """Return list of products in a purchase order."""
        return self.purchaseorderproduct_set.all()

    def order_value(self):
        total_value = Money(0, EUR)
        tv_products = self.po_products().aggregate(
            total=Sum(F('quantity_ordered') * F('unit_price'),
                      output_field=MoneyField()))
        total_value = Money(tv_products['total'], EUR) if tv_products['total']\
            else Money(0, EUR)
        return total_value


class PurchaseOrderProduct(models.Model):
    """Model for products ordered in a purchase order"""
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
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
    date_received = models.DateTimeField(blank=True, null=True)
    delivered_by = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='delivered_by_%(app_label)s_%(class)s')
    received_by = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='received_by_%(app_label)s_%(class)s',
        blank=True, null=True)

    class Meta:
        verbose_name = "Purchase order delivery"
        verbose_name_plural = "Purchase order deliveries"

    def __str__(self):
        return "{} ({})".format(self.po_product, self.quantity_delivered)

    def save(self, * args, ** kwargs):
        super(PurchaseOrderDelivery, self).save(* args, ** kwargs)
        # Update inventory items
        self.update_inventory_items()

    @property
    def items(self):
        """Return list of items at a granular level delivered by an artisan"""
        inventory = apps.get_model('inventory', 'InventoryItem')
        return inventory.objects.filter(delivery=self)

    def update_inventory_items(self):
        """Updates inventory items as per the quantity delivered"""
        inventory = apps.get_model('inventory', 'InventoryItem')
        existing_items = self.items
        qty_delivered = int(self.quantity_delivered)

        if not existing_items:
            for i in range(0, qty_delivered):
                new_serial_no = str(str(self.po_product.order.code) +
                                    str(self.po_product.id) + str(self.pk) +
                                    str(i+1).zfill(3)).lower()
                inventory.objects.create(serial_no=new_serial_no,
                                         delivery=self,
                                         product=self.po_product.product)
        else:
            count = existing_items.count()
            if count != qty_delivered:
                for i in range(count, qty_delivered):
                    new_serial_no = str(str(self.po_product.order.code) +
                                        str(self.po_product.id) +
                                        str(self.pk) + str(i+1).zfill(3)).lower()
                    inventory.objects.create(serial_no=new_serial_no,
                                             delivery=self,
                                             product=self.po_product.product)


class Workshop(models.Model):
    """Workshop model"""
    name = models.CharField(max_length=160, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Location(models.Model):
    """Geo location address"""
    name = models.CharField(max_length=160, blank=True)
    latitude = models.FloatField(default=0.00)
    longitude = models.FloatField(default=0.00)

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


class Supplier(models.Model):
    """Source of materials used in artisan production"""
    production = models.ForeignKey(ArtisanProduction, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    name = models.CharField(max_length=160, blank=True)
    address = models.TextField(blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.name)
