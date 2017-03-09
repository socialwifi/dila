import collections

TranslatedStringData = collections.namedtuple(
    'TranslatedString',
    ['pk', 'base_string', 'translation', 'comment', 'translator_comment', 'context']
)