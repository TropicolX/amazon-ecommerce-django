from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


def upload_to(instance, filename):
    return "shop/{filename}".format(filename=filename)


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(
        _("Image"), upload_to=upload_to, default="shop/default.jpg")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_products_available():
        return Product.objects.filter(available=True)

    def get_products_by_category(category_id):
        if category_id:
            return Product.objects.filter(category=category_id, available=True)
        else:
            return Product.get_products_available()
