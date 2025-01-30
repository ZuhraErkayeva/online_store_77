from django.db import models
from django.utils.text import slugify
from common.models import BaseModel


class Category(BaseModel):
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='child',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    icon = models.FileField(upload_to='categories/')
    searches = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Product(BaseModel):
    class Currency(models.TextChoices):
        USD = 'usd', 'USD'
        UZS = 'uzs', 'UZS'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        PENDING = 'pending', 'Pending'

    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    currency = models.CharField(max_length=10, default=Currency.UZS, choices=Currency.choices)
    status = models.CharField(max_length=10, default=Status.ACTIVE, choices=Status.choices)
    photos = models.ImageField(upload_to="profile_photos/", null=True, blank=True)
    searches = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return self.product
