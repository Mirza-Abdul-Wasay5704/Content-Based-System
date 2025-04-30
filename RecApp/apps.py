from django.apps import AppConfig


class RecappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'RecApp'

    def ready(self):
        import RecApp.signals
