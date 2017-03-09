from unittest import mock

import dila.application.structures
import dila.application.translations
from dila import data


def test_data_preserves_translated_strings(db_connection):
    data.add_translated_string('x', translation='y', comment='comment', translator_comment='tcomment', context='ctx')
    preserved_strings = list(data.get_translated_strings())
    assert preserved_strings == [
        dila.application.structures.TranslatedStringData(
            pk=mock.ANY,
            base_string='x',
            context='ctx',
            translation='y',
            comment='comment',
            translator_comment='tcomment',
        )]

def test_data_defaults_to_empty_translated_strings(db_connection):
    data.add_translated_string('x', translation=None, comment=None, translator_comment=None, context=None)
    preserved_strings = list(data.get_translated_strings())
    assert preserved_strings == [
        dila.application.structures.TranslatedStringData(
            pk=mock.ANY,
            base_string='x',
            context='',
            translation='',
            comment='',
            translator_comment='',
        )]
