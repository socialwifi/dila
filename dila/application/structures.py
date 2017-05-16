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


User = collections.namedtuple(
    'User',
    ['authenticated', 'username', 'first_name', 'last_name']
)
