from django.apps import AppConfig


class PanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'panel'
    verbose_name = 'پنل'

    def ready(self):
        from . import signals
        