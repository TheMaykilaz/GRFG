from rest_framework import serializers
from .models import CryptoToken

class CryptoTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoToken
        fields = ['name', 'symbol', 'price', 'percent_1h', 'percent_24h', 'percent_7d', 'market_cap', 'volume_24h']
