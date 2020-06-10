import functools

from .constants import PARSING_URLS
from .parser import parse


parsers = [
    functools.partial(parse, url, description)
    for url, description in PARSING_URLS.items()
]
