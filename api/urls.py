from django.urls import path
from .views import (
    scan_qr,
    redeem_coupon,
    analytics,
    coupon_report,
)

urlpatterns = [
    path('scan/', scan_qr),
    path('redeem/', redeem_coupon),
    path('analytics/', analytics),
    path('report/', coupon_report),
]