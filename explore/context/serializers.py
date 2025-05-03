from rest_framework import serializers
from .models import CryptoToken


class CryptoTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoToken
        fields = '__all__'
