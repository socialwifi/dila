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
LDAP_USER_BASE_DN = ''
LDAP_GROUP_OBJECT_FILTER = ''
LDAP_GROUP_BASE_DN = ''
LDAP_ENCODING = 'utf-8'
LDAP_USER_ATTRIBUTE_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
}
LDAP_START_TLS = False
LDAP_GLOBAL_OPTIONS = {}

def setup_from_module(module_name):
    module = __import__(module_name)
    setting_re = re.compile("^[A-Z0-9_]*$")
    setup(**{key: value for key, value in module.__dict__.items() if setting_re.match(key)})


def setup(**mapping):
    globals().update(mapping)
