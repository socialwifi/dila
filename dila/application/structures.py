import collections

TranslatedStringData = collections.namedtuple(
    'TranslatedString',
    ['pk', 'base_string', 'plural', 'translation', 'comment', 'translator_comment', 'context', 'resource_pk',
     'plural_translations']
)


PluralTranslations = collections.namedtuple(
    'TranslatedString',
    ['few', 'many', 'other']
)

Resource = collections.namedtuple(
    'Resource',
    ['pk', 'name']
)

Language = collections.namedtuple(
    'Language',
    ['name', 'code']
)


UserT = collections.namedtuple(
    'User',
    ['authenticated', 'username', 'first_name', 'last_name', 'is_superuser']
)

class User(UserT):
    __slots__ = ()

    def __new__(cls, authenticated, username, first_name, last_name, is_superuser=False):
        return super().__new__(cls, authenticated, username, first_name, last_name, is_superuser)