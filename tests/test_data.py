from unittest import mock

import dila.application.structures
import dila.application.translations
from dila import data


def test_adding_resource(db_connection):
    resource_pk = data.add_resource('ketchup').pk
    assert data.get_resource(resource_pk).name == 'ketchup'


def test_listing_resources(db_connection):
    data.add_resource('ketchup')
    result = list(data.get_resources())
    assert result == [dila.application.structures.Resource(
        pk=mock.ANY,
        name='ketchup',
    )]


def test_adding_language(db_connection):
    data.add_language('polish', 'pl')
    assert data.get_language('pl').name == 'polish'


def test_listing_languages(db_connection):
    data.add_language('polish', 'pl')
    result = list(data.get_languages())
    assert result == [dila.application.structures.Language(
        code='pl',
        name='polish',
    )]


def test_data_preserves_translated_strings(db_connection):
    resource_pk = data.add_resource('r').pk
    data.add_translated_string(
        resource_pk, 'x', translation='y', comment='comment', translator_comment='tcomment', context='ctx')
    preserved_strings = list(data.get_translated_strings(resource_pk))
    assert preserved_strings == [
        dila.application.structures.TranslatedStringData(
            pk=mock.ANY,
            base_string='x',
            context='ctx',
            translation='y',
            comment='comment',
            translator_comment='tcomment',
            resource_pk=resource_pk,
        )]


def test_data_defaults_to_empty_translated_strings(db_connection):
    resource_pk = data.add_resource('r').pk
    data.add_translated_string(
        resource_pk, 'x', translation=None, comment=None, translator_comment=None, context=None)
    preserved_strings = list(data.get_translated_strings(resource_pk))
    assert preserved_strings == [
        dila.application.structures.TranslatedStringData(
            pk=mock.ANY,
            base_string='x',
            context='',
            translation='',
            comment='',
            translator_comment='',
            resource_pk=resource_pk,
        )]


def test_fetching_one_translated_string(db_connection):
    resource_pk = data.add_resource('r').pk
    data.add_translated_string(
        resource_pk, 'x', translation='y', comment='comment', translator_comment='tcomment', context='ctx')
    preserved_string_pk = list(data.get_translated_strings(resource_pk))[0].pk
    preserved_string = data.get_translated_string(preserved_string_pk)
    assert preserved_string == dila.application.structures.TranslatedStringData(
            pk=preserved_string_pk,
            base_string='x',
            context='ctx',
            translation='y',
            comment='comment',
            translator_comment='tcomment',
            resource_pk=resource_pk,
        )


def test_updating_one_translated_string(db_connection):
    resource_pk = data.add_resource('r').pk
    data.add_translated_string(
        resource_pk, 'x', translation='y', comment='comment', translator_comment='tcomment', context='ctx')
    preserved_string_pk = list(data.get_translated_strings(resource_pk))[0].pk
    data.set_translated_string('pl', preserved_string_pk, translation='new')
    preserved_string = data.get_translated_string(preserved_string_pk)
    assert preserved_string == dila.application.structures.TranslatedStringData(
        pk=preserved_string_pk,
        base_string='x',
        context='ctx',
        translation='new',
        comment='comment',
        translator_comment='tcomment',
        resource_pk=resource_pk,
    )
