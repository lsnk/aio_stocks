import logging
import os
import pathlib
import sys
from importlib import import_module

SETTINGS_MODULE = os.environ.setdefault('SETTINGS_MODULE', 'settings.prod')


current_script = pathlib.Path(sys.argv[0])
PROJECT_NAME = '/'.join(current_script.parts[-2:])

print(
    f'Project `{PROJECT_NAME}` started '
    f'using `{SETTINGS_MODULE}` settings module.'
)


settings_module = import_module(SETTINGS_MODULE)


logging.basicConfig(
    level=logging.DEBUG if settings_module.DEBUG else logging.INFO,
    format='%(asctime)s | %(levelname)s: %(message)s',
)


def __getattr__(name):
    return getattr(settings_module, name)
