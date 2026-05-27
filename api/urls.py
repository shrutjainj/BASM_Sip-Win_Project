from django.urls import path

from .views import (
    scan_qr,
    redeem_coupon,
    analytics
)

# 🔐 JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    # 🚀 APIs
    path('scan/', scan_qr),
    path('redeem/', redeem_coupon),

    path('analytics/', analytics),

    # 🔐 JWT Login
    path('login/', TokenObtainPairView.as_view()),
    
    # 🔄 Refresh token
    path('refresh/', TokenRefreshView.as_view()),
]