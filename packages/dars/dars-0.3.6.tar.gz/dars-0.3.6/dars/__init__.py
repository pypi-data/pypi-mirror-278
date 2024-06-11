import pathlib
from importlib import metadata
import toml

from dars import (
        config,
        logger,
        main,
        )

logger.init()

__app_name__ = 'dars'

# --- определяем версию приложения
__version__ = 'unknown'

try:
    __version__ = metadata.version(__app_name__)
except metadata.PackageNotFoundError:
    pyproject_file = pathlib.Path(__file__).parent.parent / 'pyproject.toml'
    if pyproject_file.exists() and pyproject_file.is_file():
        __version__ = toml.load(pyproject_file)['tool']['poetry']['version']


def client(**kwargs):
    '''Инициализация клиента'''
    settings = config.Settings(**kwargs)
    return main.Client(settings)
