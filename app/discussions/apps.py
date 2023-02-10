from django.apps import AppConfig


class DiscussionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'discussions'

    def ready(self):
        import discussions.signals
