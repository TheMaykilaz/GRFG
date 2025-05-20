
import requests
from explore.models import CryptoToken

def get_top_cryptos():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        'X-CMC_PRO_API_KEY': '1efd78f7-2202-40e2-94e5-1aa842c1800c',
        'Accept': 'application/json'
    }
    params = {
        'start': '1',
        'limit': 25,
        'convert': 'USD',
        'sparkline': 'true'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
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
                    'sparkline_7d': quote['sparkline_7d']['price'],
                }
            )
        return True
    except Exception as e:
        print(f"Error fetching crypto data: {str(e)}")
        return False


if __name__ == '__main__':
    get_top_cryptos()