from django.contrib import admin
from .models import QRCode, Shop, Coupon

admin.site.register(QRCode)
admin.site.register(Shop)
admin.site.register(Coupon)