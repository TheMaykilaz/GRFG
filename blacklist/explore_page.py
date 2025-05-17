
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

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()['data']
        print(data)

        for coin in data:
            quote = coin['quote']['USD']

            # Форматуємо значення
            percent_1h = round(quote['percent_change_1h'], 2)  # 2 знаки після коми
            percent_24h = round(quote['percent_change_24h'], 2)  # 2 знаки після коми
            percent_7d = round(quote['percent_change_7d'], 2)  # 2 знаки після коми
            market_cap = int(quote['market_cap'])  # Без знаків після коми
            volume_24h = int(quote['volume_24h'])  # Без знаків після коми

            # Логування значень
            print(f"Processing {coin['symbol']}: {coin['name']} - price: {quote['price']}")

            # Зберігаємо дані в базу або оновлюємо, якщо такий символ вже є
            CryptoToken.objects.update_or_create(
                symbol=coin['symbol'],  # По символу шукаємо токен
                defaults={
                    'name': coin['name'],
                    'price': round(quote['price'], 2),  # 2 знаки після коми для ціни
                    'percent_1h': percent_1h,
                    'percent_24h': percent_24h,
                    'percent_7d': percent_7d,
                    'market_cap': market_cap,
                    'volume_24h': volume_24h,
                    'sparkline_7d': quote['sparkline_7d']['price'],
                }
            )
    else:
        print(f"Error fetching data: {response.status_code}, {response.text}")


if __name__ == '__main__':
    get_top_cryptos()