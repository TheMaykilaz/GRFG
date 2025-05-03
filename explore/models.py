from django.db import models


class CryptoToken(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    percent_1h = models.FloatField()
    percent_24h = models.FloatField()
    percent_7d = models.FloatField()
    market_cap = models.DecimalField(max_digits=25, decimal_places=2)
    volume_24h = models.DecimalField(max_digits=25, decimal_places=2)

    def __str__(self):
        return self.name


class CryptoArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)