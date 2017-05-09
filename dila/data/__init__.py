from dila.data.translated_strings import add_translated_string
from dila.data.translated_strings import get_translated_string
from dila.data.translated_strings import get_translated_strings
from dila.data.translated_strings import set_translated_string
from dila.data.resources import add_resource
from dila.data.resources import get_resource
from dila.data.resources import get_resources
from dila.data.engine import setup
from dila.data.engine import shutdown_session


def add_language(name, code):
    pass


def get_languages():
    return []


def get_language(code):
    return ''


__all__ = [
    add_translated_string, get_translated_string, get_translated_strings, set_translated_string, add_resource,
    get_resource, get_resources, setup, shutdown_session, add_language, get_languages, get_language,
]
