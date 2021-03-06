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
    data.add_language('polish', 'pl')
    resource_pk = data.add_resource('r').pk
    string_pk = data.add_or_update_base_string(resource_pk, 'x', comment='comment', context='ctx')
    data.set_translated_string('pl', string_pk, translation='y', translator_comment='tcomment')
    preserved_strings = list(data.get_translated_strings('pl', resource_pk))
    assert preserved_strings == [
        dila.application.structures.TranslatedStringData(
            pk=mock.ANY,
            base_string='x',
            plural='',
            context='ctx',
            translation='y',
            comment='comment',
            translator_comment='tcomment',
            resource_pk=resource_pk,
            plural_translations=None,
        )]


def test_adding_the_same_sting(db_connection):
    data.add_language('polish', 'pl')
    resource_pk = data.add_resource('r').pk
    data.add_or_update_base_string(resource_pk, 'x', comment='comment', context='ctx')
    data.add_or_update_base_string(resource_pk, 'x', comment='lolz', context='ctx')
    preserved_strings = list(data.get_translated_strings('pl', resource_pk))
    assert preserved_strings == [
        dila.application.structures.TranslatedStringData(
            pk=mock.ANY,
            base_string='x',
            plural='',
            context='ctx',
            translation='',
            comment='lolz',
            translator_comment='',
            resource_pk=resource_pk,
            plural_translations=None,
        )]


def test_adding_the_same_sting_without_context(db_connection):
    data.add_language('polish', 'pl')
    resource_pk = data.add_resource('r').pk
    data.add_or_update_base_string(resource_pk, 'x', comment='comment', context=None)
    data.add_or_update_base_string(resource_pk, 'x', comment='lolz', context=None)
    preserved_strings = list(data.get_translated_strings('pl', resource_pk))
    assert preserved_strings == [
        dila.application.structures.TranslatedStringData(
            pk=mock.ANY,
            base_string='x',
            plural='',
            context='',
            translation='',
            comment='lolz',
            translator_comment='',
            resource_pk=resource_pk,
            plural_translations=None,
        )]


def test_data_defaults_to_empty_translated_strings(db_connection):
    data.add_language('polish', 'pl')
    resource_pk = data.add_resource('r').pk
    data.add_or_update_base_string(resource_pk, 'x', comment=None, context=None)
    preserved_strings = list(data.get_translated_strings('pl', resource_pk))
    assert preserved_strings == [
        dila.application.structures.TranslatedStringData(
            pk=mock.ANY,
            base_string='x',
            plural='',
            context='',
            translation='',
            comment='',
            translator_comment='',
            resource_pk=resource_pk,
            plural_translations=None,
        )]


def test_fetching_one_untranslated_string(db_connection):
    data.add_language('polish', 'pl')
    resource_pk = data.add_resource('r').pk
    string_pk = data.add_or_update_base_string(resource_pk, 'x', comment='comment', context='ctx')
    preserved_string = data.get_translated_string('pl', string_pk)
    assert preserved_string == dila.application.structures.TranslatedStringData(
            pk=string_pk,
            base_string='x',
            plural='',
            context='ctx',
            translation='',
            comment='comment',
            translator_comment='',
            resource_pk=resource_pk,
            plural_translations=None,
        )


def test_fetching_one_plural_untranslated_string(db_connection):
    data.add_language('polish', 'pl')
    resource_pk = data.add_resource('r').pk
    string_pk = data.add_or_update_base_string(resource_pk, 'one x', plural='%d xs', comment='comment', context='ctx')
    preserved_string = data.get_translated_string('pl', string_pk)
    assert preserved_string == dila.application.structures.TranslatedStringData(
            pk=string_pk,
            base_string='one x',
            plural='%d xs',
            context='ctx',
            translation='',
            comment='comment',
            translator_comment='',
            resource_pk=resource_pk,
            plural_translations=dila.application.structures.PluralTranslations(
                few='',
                many='',
                other='',
            ),
        )


def test_fetching_one_plural_translated_string(db_connection):
    data.add_language('polish', 'pl')
    resource_pk = data.add_resource('r').pk
    string_pk = data.add_or_update_base_string(resource_pk, 'one x', plural='%d xs', comment='comment', context='ctx')
    data.set_translated_string('pl', string_pk, translation='jeden iks', translator_comment='tcomment',
                               plural_translations=dila.application.structures.PluralTranslations(
                                   few='%d iksy',
                                   many='%d iksów',
                                   other='%d iksów',
                               ))
    data.shutdown_session()
    preserved_string = data.get_translated_string('pl', string_pk)
    assert preserved_string == dila.application.structures.TranslatedStringData(
        pk=string_pk,
        base_string='one x',
        plural='%d xs',
        context='ctx',
        translation='jeden iks',
        comment='comment',
        translator_comment='tcomment',
        resource_pk=resource_pk,
        plural_translations=dila.application.structures.PluralTranslations(
           few='%d iksy',
           many='%d iksów',
           other='%d iksów',
        ),
    )


def test_fetching_one_translated_string(db_connection):
    data.add_language('polish', 'pl')
    resource_pk = data.add_resource('r').pk
    string_pk = data.add_or_update_base_string(resource_pk, 'x', comment='comment', context='ctx')
    data.set_translated_string('pl', string_pk, translation='y', translator_comment='tcomment')
    preserved_string = data.get_translated_string('pl', string_pk)
    assert preserved_string == dila.application.structures.TranslatedStringData(
            pk=string_pk,
            base_string='x',
            plural='',
            context='ctx',
            translation='y',
            comment='comment',
            translator_comment='tcomment',
            resource_pk=resource_pk,
            plural_translations=None,
        )


def test_updating_one_translated_string(db_connection):
    data.add_language('polish', 'pl')
    resource_pk = data.add_resource('r').pk
    string_pk = data.add_or_update_base_string(
        resource_pk, 'x', comment='comment', context='ctx')
    data.set_translated_string('pl', string_pk, translation='y', translator_comment='tcomment')
    data.set_translated_string('pl', string_pk, translation='new')
    preserved_string = data.get_translated_string('pl', string_pk)
    assert preserved_string == dila.application.structures.TranslatedStringData(
        pk=string_pk,
        base_string='x',
        plural='',
        context='ctx',
        translation='new',
        comment='comment',
        translator_comment='tcomment',
        resource_pk=resource_pk,
        plural_translations=None,
    )


def test_updating_one_plural_translated_string(db_connection):
    data.add_language('polish', 'pl')
    resource_pk = data.add_resource('r').pk
    string_pk = data.add_or_update_base_string(resource_pk, 'one x', plural='%d xs', comment='comment', context='ctx')
    data.set_translated_string('pl', string_pk, translation='jeden x', translator_comment='tcomment',
                               plural_translations=dila.application.structures.PluralTranslations(
                                   few='%d x',
                                   many='%d x',
                                   other='%d x',
                               ))
    data.set_translated_string('pl', string_pk, translation='jeden iks', translator_comment='tcomment',
                               plural_translations=dila.application.structures.PluralTranslations(
                                   few='%d iksy',
                                   many='%d iksów',
                                   other='%d iksów',
                               ))
    preserved_string = data.get_translated_string('pl', string_pk)
    data.shutdown_session()
    assert preserved_string == dila.application.structures.TranslatedStringData(
        pk=string_pk,
        base_string='one x',
        plural='%d xs',
        context='ctx',
        translation='jeden iks',
        comment='comment',
        translator_comment='tcomment',
        resource_pk=resource_pk,
        plural_translations=dila.application.structures.PluralTranslations(
            few='%d iksy',
            many='%d iksów',
            other='%d iksów',
        ),
    )


def test_translating_string_into_multiple_languages(db_connection):
    data.add_language('polish', 'pl')
    data.add_language('dutch', 'nl')
    resource_pk = data.add_resource('r').pk
    string_pk = data.add_or_update_base_string(
        resource_pk, 'x', comment='comment', context='ctx')
    data.set_translated_string('pl', string_pk, translation='y', translator_comment='ytcomment')
    data.set_translated_string('nl', string_pk, translation='z', translator_comment='ztcomment')
    first_string = data.get_translated_string('pl', string_pk)
    second_string = data.get_translated_string('nl', string_pk)
    assert first_string == dila.application.structures.TranslatedStringData(
        pk=string_pk,
        base_string='x',
        plural='',
        context='ctx',
        translation='y',
        comment='comment',
        translator_comment='ytcomment',
        resource_pk=resource_pk,
        plural_translations=None,
    )
    assert second_string == dila.application.structures.TranslatedStringData(
        pk=string_pk,
        base_string='x',
        plural='',
        context='ctx',
        translation='z',
        comment='comment',
        translator_comment='ztcomment',
        resource_pk=resource_pk,
        plural_translations=None,
    )


def test_deleting_old_strings(db_connection):
    resource_pk = data.add_resource('r').pk
    first_string_pk = data.add_or_update_base_string(resource_pk, 'x', comment='comment', context='ctx')
    data.add_or_update_base_string(resource_pk, 'y', comment='comment', context='ctx')
    data.delete_old_strings(resource_pk, keep_pks=[first_string_pk])
    preserved_strings = list(data.get_translated_strings('pl', resource_pk))
    assert preserved_strings == [
        dila.application.structures.TranslatedStringData(
            pk=mock.ANY,
            base_string='x',
            plural='',
            context='ctx',
            translation='',
            comment='comment',
            translator_comment='',
            resource_pk=resource_pk,
            plural_translations=None,
        )]


def test_deleting_old_translated_strings(db_connection):
    data.add_language('polish', 'pl')
    resource_pk = data.add_resource('r').pk
    first_string_pk = data.add_or_update_base_string(resource_pk, 'x', comment='comment', context='ctx')
    second_string_pk = data.add_or_update_base_string(resource_pk, 'y', comment='comment', context='ctx')
    data.set_translated_string('pl', second_string_pk, translation='y', translator_comment='ytcomment')
    data.delete_old_strings(resource_pk, keep_pks=[first_string_pk])
    preserved_strings = list(data.get_translated_strings('pl', resource_pk))
    assert preserved_strings == [
        dila.application.structures.TranslatedStringData(
            pk=mock.ANY,
            base_string='x',
            plural='',
            context='ctx',
            translation='',
            comment='comment',
            translator_comment='',
            resource_pk=resource_pk,
            plural_translations=None,
        )]


def test_data_preserves_po_metadata(db_connection):
    data.add_language('polish', 'pl')
    resource_pk = data.add_resource('r').pk
    data.update_po_metadata('pl', resource_pk, {'meta1': 'x'})
    data.shutdown_session()
    assert data.get_po_metadata('pl', resource_pk) == {'meta1': 'x'}
