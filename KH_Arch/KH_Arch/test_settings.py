from .settings import *

# Utiliser SQLite en mémoire pour les tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


# Désactiver la migration pendant les tests pour accélérer l'exécution
# class DisableMigrations:
#     def __contains__(self, item):
#         return True
#
#     def __getitem__(self, item):
#         return None
#
#
# MIGRATION_MODULES = DisableMigrations()

# Vous pouvez également désactiver ou configurer d'autres éléments pour les tests,
# comme le système de cache, les services de messagerie, etc.
