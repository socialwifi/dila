import contextlib

import ldap
from ldap import filter as ldap_filter

from dila import config
from dila.application import structures

ANONYMOUS_USER = structures.User(authenticated=False, username='', first_name='ANONYMOUS', last_name='')


def authenticate(username, password):
    records = get_user_records(username)
    if records:
        user_dn, user_attributes = records[0]
        with initialize_connection() as connection:
            try:
                connection.simple_bind_s(user_dn, password)
            except ldap.LDAPError:
                return ANONYMOUS_USER
            else:
                encoding = config.LDAP_ENCODING
                first_name = user_attributes.get(config.LDAP_USER_ATTRIBUTE_MAP['first_name'])[0].decode(encoding)
                last_name = user_attributes.get(config.LDAP_USER_ATTRIBUTE_MAP['last_name'])[0].decode(encoding)
                return structures.User(
                    authenticated=True, username=username, first_name=first_name, last_name=last_name)
    else:
        return ANONYMOUS_USER


def get_user_records(username):
    with initialize_connection() as connection:
        connection.simple_bind_s(config.LDAP_BIND_DN, config.LDAP_BIND_PASSWORD)
        query = config.LDAP_USER_OBJECT_FILTER % {'user': ldap_filter.escape_filter_chars(username)}
        records = connection.search_s(config.LDAP_USER_BASE_DN, ldap.SCOPE_SUBTREE, query)
    return records


@contextlib.contextmanager
def initialize_connection():
    connection = ldap.initialize(config.LDAP_SERVER_URI)
    connection.protocol_version = ldap.VERSION3
    for key, value in config.LDAP_GLOBAL_OPTIONS.items():
        connection.set_option(key, value)
    if config.LDAP_START_TLS:
        connection.start_tls_s()
    yield connection
    connection.unbind_s()
