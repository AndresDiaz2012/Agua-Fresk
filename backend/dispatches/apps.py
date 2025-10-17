from django.apps import AppConfig


class DispatchesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dispatches'

    def ready(self):
        # Import signals
        from . import signals  # noqa: F401
