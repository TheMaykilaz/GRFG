
from django.core.management.base import BaseCommand
from blacklist.explore_page import get_top_cryptos

class Command(BaseCommand):
    help = "Update crypto data"

    def handle(self, *args, **kwargs):
        get_top_cryptos()
        self.stdout.write("Crypto data updated.")
