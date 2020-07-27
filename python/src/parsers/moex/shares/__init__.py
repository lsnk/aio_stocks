import functools

from .constants import PARSING_URLS
from ..parser import parse


# TODO: выделить общий базовый класс для парсеров
parsers = [
    functools.partial(parse, url, description)
    for url, description in PARSING_URLS.items()
]
