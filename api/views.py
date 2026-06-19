from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.http import JsonResponse
from .models import QRCode, Shop, Coupon, Product
import uuid
import numpy as np
import pandas as pd

@api_view(['GET'])
def home(request):
    return Response({
        "message" : "JAI BOLO SHRI AADINATH BHAGWAAN KI JAI HO JAI JAI JAI"
    })
# 🚀 QR SCAN API
@api_view(['POST'])
def scan_qr(request):

    # 🔹 Frontend se QR code
    code = request.data.get("code")

    # 🔹 Frontend se selected product
    product_name = request.data.get("product")

    try:

        # 🔹 QR database me find karo
        qr = QRCode.objects.get(code=code)

        # 🔹 QR already used?
        if qr.is_used:
            return Response({
                "error": "QR already used"
            })

        # 🔹 Product find
        product = Product.objects.filter(
            name=product_name
        ).first()

        # 🔹 Product not found
        if not product:
            return Response({
                "error": "Invalid product"
            })

        # 🔹 Event based shop filtering
        if qr.event:

            shops = qr.event.shops.filter(
                category=product.category
            )

        else:

            shops = Shop.objects.filter(
                category=product.category
            )

        # 🔹 No shops
        if not shops.exists():
            return Response({
                "error": "No shop available"
            })

        # 🔹 Random shop select
        shop = shops.order_by('?').first()

        # 🔹 Safety check
        if not shop:
            return Response({
                "error": "Shop not found"
            })

        # 🔹 Unique coupon code
        coupon_code = str(uuid.uuid4())[:8]

        # 🔹 Coupon create
        coupon = Coupon.objects.create(
            qr=qr,
            shop=shop,
            code=coupon_code
        )

        # 🔹 QR mark used
        qr.is_used = True
        qr.save()

        # 🔹 Final response
        return Response({

            "message": "Coupon generated successfully",

            "product": product.name,

            "shop": shop.name,

            "location": shop.location,

            "discount": shop.discount,

            "coupon": coupon.code

        })

    # 🔹 Invalid QR
    except QRCode.DoesNotExist:

        return Response({
            "error": "Invalid QR"
        })


# 🚀 COUPON REDEEM API
@api_view(['POST'])
@permission_classes([IsAuthenticated])

def redeem_coupon(request):

    # 🔹 Coupon code frontend se
    code = request.data.get("code")

    try:

        # 🔹 Coupon find
        coupon = Coupon.objects.get(code=code)

        # 🔹 Shop ownership check
        if coupon.shop.user != request.user:

            return Response({
                "error": "Not your coupon"
            })

        # 🔹 Already redeemed?
        if coupon.is_used:

            return Response({
                "error": "Coupon already used"
            })

        # 🔹 Redeem
        coupon.is_used = True

        # 🔹 Save
        coupon.save()

        return Response({

            "message": "Coupon redeemed successfully",

            "shop": coupon.shop.name,

            "coupon": coupon.code

        })

    # 🔹 Invalid coupon
    except Coupon.DoesNotExist:

        return Response({
            "error": "Invalid coupon"
        })


# 🚀 ANALYTICS API
@api_view(['GET'])
def analytics(request):

    total_qr = QRCode.objects.count()

    total_coupons = Coupon.objects.count()

    redeemed = Coupon.objects.filter(
        is_used=True
    ).count()

    active = Coupon.objects.filter(
        is_used=False
    ).count()

    redemption_rate = (
        np.divide(redeemed, total_coupons) * 100
        if total_coupons > 0
        else 0
    )

    coupons = Coupon.objects.all().values(
        "shop__name",
        "is_used"
    )

    df = pd.DataFrame(coupons)

    shop_ranking = []

    if not df.empty:

        shop_stats = (
            df.groupby("shop__name")["is_used"]
            .agg(["count", "sum"])
            .reset_index()
        )

        shop_stats.columns = [
            "shop",
            "total_coupons",
            "redeemed"
        ]

        shop_stats["active"] = (
            shop_stats["total_coupons"]
            - shop_stats["redeemed"]
        )

        shop_stats["redemption_rate"] = (
            shop_stats["redeemed"]
            / shop_stats["total_coupons"]
            * 100
        ).round(2)

        shop_ranking = shop_stats.to_dict(
            orient="records"
        )

    return Response({
        "total_qr": total_qr,
        "total_coupons": total_coupons,
        "redeemed": redeemed,
        "active": active,
        "redemption_rate": round(redemption_rate, 2),
        "shop_ranking": shop_ranking
    })

@api_view(['GET'])
def coupon_report(request):
    total = Coupon.objects.count()

    redeemed = Coupon.objects.filter(
        is_used = True
    ).count()

    active = Coupon.objects.filter(
        is_used = False
    ).count()

    redemption_rate = (redeemed / total * 100 if total > 0 else 0)

    return Response({
        "total_coupons" : total,
        "redeemed" : redeemed,
        "active" : active,
        "redemption_rate" : round(redemption_rate, 2)
    })