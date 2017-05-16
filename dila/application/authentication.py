import contextlib

import ldap
from ldap import filter as ldap_filter

from dila import config


def authenticate(username, password):
    records = get_user_records(username)
    if records:
        user_dn, user_attributes = records[0]
        with initialize_connection() as connection:
            try:
                connection.simple_bind_s(user_dn, password)
            except ldap.LDAPError:
                return False
            else:
                return True
    else:
        return False


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
    yield connection
    connection.unbind_s()
