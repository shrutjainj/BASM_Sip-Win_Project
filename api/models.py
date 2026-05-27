from django.db import models

# 🔐 Django User
from django.contrib.auth.models import User


# 🚀 QR Code
class QRCode(models.Model):

    code = models.CharField(
        max_length=100,
        unique=True
    )

    is_used = models.BooleanField(
        default=False
    )

    # ✅ Event link
    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.code


# 🚀 Shop
class Shop(models.Model):

    # ✅ LOGIN USER
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=200)

    category = models.CharField(max_length=100)

    location = models.CharField(max_length=1000)

    discount = models.IntegerField()

    owner_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


# 🚀 Coupon
class Coupon(models.Model):

    qr = models.ForeignKey(
        QRCode,
        on_delete=models.CASCADE
    )

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE
    )

    code = models.CharField(max_length=50)

    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.code


# 🚀 Product
class Product(models.Model):

    name = models.CharField(max_length=100)

    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 🚀 Event
class Event(models.Model):

    name = models.CharField(max_length=100)

    location = models.CharField(max_length=100)

    date = models.DateField()

    shops = models.ManyToManyField(Shop)

    def __str__(self):
        return self.name