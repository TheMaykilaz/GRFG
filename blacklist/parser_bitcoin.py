import requests
import pandas as pd

def get_cryptocurrency_dominance():
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"
    headers = {
        'X-CMC_PRO_API_KEY': '1efd78f7-2202-40e2-94e5-1aa842c1800c',
        'Accept': 'application/json',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        dominance_dict = [{
            "BTC": f"{data['data']['btc_dominance']:.1f}",
            "ETH": f"{data['data']['eth_dominance']:.1f}",
            "ALT": f"{100 - data['data']['btc_dominance'] - data['data']['eth_dominance']:.1f}",
        }]
        dom_t = pd.DataFrame(dominance_dict).T.reset_index()
        dom_t.columns = ['Coin', 'Dominance (%)']

        return dom_t

    else:
        print(f"Error: {response.status_code}")
        return None

def get_total_dominance():
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"
    headers = {
        'X-CMC_PRO_API_KEY': '1efd78f7-2202-40e2-94e5-1aa842c1800c',
        'Accept': 'application/json',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        total_market_cap_usd = data['data']['quote']['USD']['total_market_cap']
        total_market_cap_usd = int(total_market_cap_usd)
        if total_market_cap_usd > 1000000000000:
            total_market_cap_usd = str(total_market_cap_usd)
            total_market_cap_usd = total_market_cap_usd[0] + ',' + total_market_cap_usd[1:3] + 'T'
            return total_market_cap_usd
    else:
        print(f"Error: {response.status_code}")
        return None


def get_fear_and_greed():
    url = "https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '1efd78f7-2202-40e2-94e5-1aa842c1800c'
    }

    params = {
        'limit': 1
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()['data'][0]
        value = data['value']
        classfication = data['value_classification']
        return value, f'{classfication}'

    else:
        print(f"Error fetching Fear & Greed Index: {response.status_code}")
        return None


if __name__ == "__main__":
    get_cryptocurrency_dominance()
    get_total_dominance()
    get_fear_and_greed()
