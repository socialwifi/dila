import re

SERVER_NAME = None
SECRET_KEY = None
ENV = 'production'
DEBUG = False
DATABASE_URL = ''
STATIC_URL = ''
LDAP_SERVER_URI = ''
LDAP_BIND_DN = ''
LDAP_BIND_PASSWORD = ''
LDAP_USER_OBJECT_FILTER = ''
LDAP_BASE_DN = ''


def setup_from_module(module_name):
    module = __import__(module_name)
    setting_re = re.compile("^[A-Z0-9_]*$")
    setup(**{key: value for key, value in module.__dict__.items() if setting_re.match(key)})


def setup(**mapping):
    globals().update(mapping)
