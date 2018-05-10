"""
Validation models
"""
from django.db import models
from django.core.validators import MinValueValidator
from apps.shared.audit_log.models.fields import CreatingUserField
from apps.shared.audit_log.models.fields import LastUserField
from apps.inventory.models import InventoryItem
from apps.users.models import User
from apps.purchases.models import Workshop


class Validation(models.Model):
    """Validation model"""
    PRODUCTION_STAGE = (
        ('artisan_production', 'Artisan Production'),
        ('in_house_wip', 'In-house WIP'),
    )
    item = models.OneToOneField(InventoryItem, on_delete=models.PROTECT)
    is_approved = models.BooleanField(default=False)
    date_validated = models.DateTimeField(auto_now=True)
    delivered_by = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='validated_by_%(app_label)s_%(class)s')

    stage = models.CharField(choices=PRODUCTION_STAGE,
                             default='artisan_production', max_length=160)

    def __str__(self):
        return "{} ({})".format(self.item, self.is_approved)


class WorkInProgress(models.Model):
    """Work In Progress (WIP)

    Tracks processing of products / items from Artisan Production and
    InHouse value addition
    """
    PROCESS = (
        ('electroplating', 'Electroplating'),
        ('modification', 'Modification'),
        ('assembly', 'Assembly'),
    )

    workshop = models.ForeignKey(Workshop, on_delete=models.PROTECT)
    quantity_received = models.FloatField(
        validators=[MinValueValidator(0.00), ], default=0.00)
    date_received = models.DateTimeField()
    quantity_delivered = models.FloatField(
        validators=[MinValueValidator(0.00), ], default=0.00)
    date_delivered = models.DateTimeField()
    process = models.CharField(choices=PROCESS,
                               default='artisan_production', max_length=160)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = CreatingUserField(
        related_name="created_by_%(app_label)s_%(class)s",
        on_delete=models.PROTECT)
    modified_by = LastUserField(
        related_name='modified_by_%(app_label)s_%(class)s',
        on_delete=models.PROTECT)

    def __str__(self):
        return
