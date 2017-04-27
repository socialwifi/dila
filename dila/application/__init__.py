from .meta import setup
from .meta import shutdown_session
from .translations import get_po_file
from .translations import get_translated_string
from .translations import get_translated_strings
from .translations import set_translated_string
from .translations import upload_translated_po_file


def add_resource(resource_name):
    pass


__all__ = [setup, shutdown_session, upload_translated_po_file, get_translated_string, get_translated_strings,
           set_translated_string, get_po_file, add_resource]
