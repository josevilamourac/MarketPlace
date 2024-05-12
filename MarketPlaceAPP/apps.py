from django.apps import AppConfig


class MarketPlaceAPPConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MarketPlaceAPP'


def ready(self):
    import MarketPlaceAPP.signals
