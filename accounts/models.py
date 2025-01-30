from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from common.validators import validate_phone
from common.models import Region, District
# from products.models import Category
from .managers import UserManager


class Address(models.Model):
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=10, decimal_places=2)
    long = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        SELLER = 'seller', 'Seller'
        ADMIN = 'admin', 'Admin'

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(max_length=12, unique=True, validators=[validate_phone])
    full_name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    profile_photo = models.ImageField(upload_to='accounts/', null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='users', null=True)
    role = models.CharField(max_length=10, null=True, blank=True, choices=Role.choices)
    project_name = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey("products.Category", on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number
