SECRET_KEY = 'secret'
DEBUG = True
DATABASE_URL = 'postgresql://dila:dila@db/dila'
LDAP_SERVER_URI = 'ldap://ldap'
LDAP_BIND_DN = 'cn=admin,dc=example,dc=com'
LDAP_BIND_PASSWORD = 'admin_password'
LDAP_BASE_DN = 'ou=employees,dc=example,dc=com'
LDAP_USER_OBJECT_FILTER = "(|(uid=%(user)s)(mail=%(user)s))"
