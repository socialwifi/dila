import collections

TranslatedStringData = collections.namedtuple(
    'TranslatedString',
    ['base_string', 'translation', 'comment', 'translator_comment', 'context']
)
