import collections

TranslatedStringData = collections.namedtuple(
    'TranslatedString',
    ['pk', 'base_string', 'translation', 'comment', 'translator_comment', 'context', 'resource_pk']
)

Resource = collections.namedtuple(
    'Resource',
    ['pk', 'name']
)

Language = collections.namedtuple(
    'Language',
    ['name', 'code']
)
