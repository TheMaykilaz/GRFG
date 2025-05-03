from django.apps import AppConfig

class ExploreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'explore'

    def ready(self):
        from django.conf import settings
        if settings.DEBUG:
            try:
                from .utils import fetch_and_update_cryptos
                fetch_and_update_cryptos()
            except Exception as e:
                print(f"[ERROR] fetch_and_update_cryptos failed: {e}")
