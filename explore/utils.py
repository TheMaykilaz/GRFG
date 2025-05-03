import requests
from .models import CryptoToken

def fetch_and_update_cryptos():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        'X-CMC_PRO_API_KEY': '1efd78f7-2202-40e2-94e5-1aa842c1800c',
        'Accept': 'application/json'
    }
    params = {
        'start': '1',
        'limit': 25,
        'convert': 'USD'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()['data']

        for coin in data:
            quote = coin['quote']['USD']

            CryptoToken.objects.update_or_create(
                symbol=coin['symbol'],
                defaults={
                    'name': coin['name'],
                    'price': round(quote['price'], 2),
                    'percent_1h': round(quote['percent_change_1h'], 2),
                    'percent_24h': round(quote['percent_change_24h'], 2),
                    'percent_7d': round(quote['percent_change_7d'], 2),
                    'market_cap': int(quote['market_cap']),
                    'volume_24h': int(quote['volume_24h']),
                }
            )
