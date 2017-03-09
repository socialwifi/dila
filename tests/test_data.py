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


def test_fetching_one_translated_string(db_connection):
    data.add_translated_string('x', translation='y', comment='comment', translator_comment='tcomment', context='ctx')
    preserved_string_pk = list(data.get_translated_strings())[0].pk
    preserved_string = data.get_translated_string(preserved_string_pk)
    assert preserved_string == dila.application.structures.TranslatedStringData(
            pk=preserved_string_pk,
            base_string='x',
            context='ctx',
            translation='y',
            comment='comment',
            translator_comment='tcomment',
        )

def test_updating_one_translated_string(db_connection):
    data.add_translated_string('x', translation='y', comment='comment', translator_comment='tcomment', context='ctx')
    preserved_string_pk = list(data.get_translated_strings())[0].pk
    data.set_translated_string(preserved_string_pk, translation='new')
    preserved_string = data.get_translated_string(preserved_string_pk)
    assert preserved_string == dila.application.structures.TranslatedStringData(
        pk=preserved_string_pk,
        base_string='x',
        context='ctx',
        translation='new',
        comment='comment',
        translator_comment='tcomment',
    )
