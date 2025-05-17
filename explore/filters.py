import django_filters
from .models import CryptoToken

class CryptoTokenFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = CryptoToken
        fields = ['price_min', 'price_max']