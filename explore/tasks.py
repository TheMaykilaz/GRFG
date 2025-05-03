from celery import shared_task
from blacklist.explore_page import get_top_cryptos

@shared_task
def update_crypto_data():
    get_top_cryptos()