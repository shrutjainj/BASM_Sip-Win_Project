from rest_framework import serializers
from .models import *

class QRSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = '__all__'