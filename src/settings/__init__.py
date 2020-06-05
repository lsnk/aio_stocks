import os
from importlib import import_module

SETTINGS_MODULE = os.environ.setdefault('SETTINGS_MODULE', 'settings.prod')

print(f'Project started using `{SETTINGS_MODULE}` settings module.')


settings_module = import_module(SETTINGS_MODULE)


def __getattr__(name):
    return getattr(settings_module, name)
