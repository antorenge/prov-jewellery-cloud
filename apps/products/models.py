"""
Models for products
"""
from django.db import models
from django.apps import apps
from django.core.validators import MinValueValidator
from apps.shared.audit_log.models.fields import CreatingUserField
from apps.shared.audit_log.models.fields import LastUserField
from apps.users.models import User


class ProductDesign(models.Model):
    """Product design

    Details a products design and specifications.
    """
    sku = models.CharField(unique=True, verbose_name='SKU', primary_key=True,
                           db_index=True, max_length=64, blank=True)
    name = models.CharField(max_length=160, blank=True)
    collection = models.CharField(blank=True, max_length=160)
    category = models.CharField(blank=True, max_length=160)
    year = models.PositiveIntegerField()
    variance = models.CharField(blank=True, max_length=2)
    color = models.CharField(blank=True, max_length=3)
    size = models.CharField(blank=True, max_length=4)
    shape = models.CharField(blank=True, max_length=24)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = CreatingUserField(
        related_name="created_by_%(app_label)s_%(class)s",
        on_delete=models.PROTECT)
    modified_by = LastUserField(
        related_name='modified_by_%(app_label)s_%(class)s',
        on_delete=models.PROTECT)
    components = models.ManyToManyField('self', through='Component',
                                        symmetrical=False,
                                        related_name='product_components')
    bill_of_materials = models.ManyToManyField('Material',
                                               through='BillOfMaterial')
    designers = models.ManyToManyField(User)

    def __str__(self):
        return "{} {}".format(self.sku, self.name)

    def save(self, * args, ** kwargs):

        if not self.sku:
            product_model = apps.get_model('products', 'ProductDesign')
            count = product_model.objects.count()
            self.sku = str(str(self.variance)[:2] + str(self.year)[-2:] +
                           str(self.color)[:3] + str(self.size)[:4] +
                           str(count + 1)).upper()

        super(ProductDesign, self).save(* args, ** kwargs)

    @property
    def default_image(self):
        """Return a product default image"""
        image_model = apps.get_model('products', 'Image')
        return image_model.objects.filter(product=self).first()


class Component(models.Model):
    """Product design components"""
    parent = models.ForeignKey(ProductDesign, on_delete=models.PROTECT,
                               related_name='parent_product')
    child = models.ForeignKey(ProductDesign, on_delete=models.PROTECT,
                              related_name='child_product')
    quantity = models.FloatField(validators=[MinValueValidator(0.00), ],
                                 default=0.00)

    def __str__(self):
        return "{} ({})".format(self.child, self.quantity)


class Drawing(models.Model):
    """Product design drawings"""
    product = models.ForeignKey(
        ProductDesign, related_name='drawings', on_delete=models.CASCADE)
    file = models.ImageField(
        upload_to='images/products/%Y/%m',
        default='images/products/None/no-img.png')
    label = models.CharField(max_length=160, blank=True, null=True)


class Image(models.Model):
    """Product design images"""
    product = models.ForeignKey(
        ProductDesign, related_name='images', on_delete=models.CASCADE)
    file = models.ImageField(
        upload_to='images/products/%Y/%m',
        default='images/products/None/no-img.png')
    label = models.CharField(max_length=160, blank=True, null=True)


class Dimension(models.Model):
    """Product design dimensions and specifications"""
    product = models.ForeignKey(ProductDesign, on_delete=models.CASCADE)
    attribute = models.CharField(blank=True, max_length=160)
    measurement = models.CharField(max_length=160, blank=True)

    def __str__(self):
        return "{} ({})".format(self.attribute, self.measurement)


class Technique(models.Model):
    """Techniques"""
    name = models.CharField(blank=True, null=True, max_length=160)

    def __str__(self):
        return "{}".format(self.name)


class Material(models.Model):
    """Materials"""
    name = models.CharField(blank=True, null=True, max_length=160)
    units_of_measurement = models.CharField(max_length=160, default=None)
    techniques = models.ManyToManyField('Technique',
                                        through='MaterialTechnique')

    def __str__(self):
        return "{} ({})".format(self.name, self.units_of_measurement)


class BillOfMaterial(models.Model):
    """Product design bill of materials"""
    product = models.ForeignKey(ProductDesign, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField(validators=[MinValueValidator(0.00), ],
                                 default=0.00)

    def __str__(self):
        return "{} ({})".format(self.material, self.quantity)


class MaterialTechnique(models.Model):
    """Material techniques"""
    SKILL_LEVELS = (
        ('basic', 'Basic'),
        ('special', 'Special'),
        ('auxilliary', 'Auxilliary'),
    )
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    technique = models.ForeignKey(Technique, on_delete=models.CASCADE)
    level = models.CharField(choices=SKILL_LEVELS, default='basic',
                             max_length=160)
    complexity = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.technique)
