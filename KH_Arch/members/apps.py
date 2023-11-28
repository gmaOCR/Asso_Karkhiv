from django.apps import AppConfig


class MembersConfig(AppConfig):
    name = 'members'

    def ready(self):
        import members.signals


class ArchitectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'members'
