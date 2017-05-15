from unittest import mock

import itertools

import dila.application.resources
from dila.application import structures

from dila import application

test_po = '''
msgid ""
msgstr ""
"x: y\\n"

# My comment
#. Programmer comment
#: location.c:23
#, fuzzy
msgctxt "Disambiguation for context"
msgid "Yellow"
msgstr "Żółć"
'''

test_plural_po = '''
#. Programmer comment
#: location.c:120
#, python-format
msgid "%d option"
msgid_plural "%d options"
msgstr[0] "%d opcję"
msgstr[1] "%d opcje"
msgstr[2] "%d opcji"
msgstr[3] "%d opcji"
'''

test_result_po = '''#
msgid ""
msgstr "x: y\\n"

#. Programmer comment
# My comment
msgctxt "Disambiguation for context"
msgid "Yellow"
msgstr "Żółć"
'''

test_result_plural_po = '''#
msgid ""
msgstr ""

#. Programmer comment
msgctxt ""
msgid "%d option"
msgid_plural "%d options"
msgstr[0] "%d opcję"
msgstr[1] "%d opcje"
msgstr[2] "%d opcji"
msgstr[3] "%d opcji"
'''


@mock.patch('dila.data.add_resource')
def test_add_resource(add_resource):
    dila.application.add_resource('Next')
    assert add_resource.mock_calls == [
        mock.call(
            'Next',
        )]


@mock.patch('dila.data.get_resources')
def test_get_resources(get_resources):
    get_resources.return_value = ['data_result']
    result = application.get_resources()
    get_resources.assert_called_with()
    assert result == ['data_result']


@mock.patch('dila.data.get_resources')
def test_get_resources_evaluates_iterator(get_resources):
    get_resources.return_value = itertools.repeat(0, 0)
    result = application.get_resources()
    assert result == []


@mock.patch('dila.data.get_resource')
def test_get_resource(get_resource):
    get_resource.return_value = 'data_result'
    result = application.get_resource('pk')
    get_resource.assert_called_with('pk')
    assert result == 'data_result'


@mock.patch('dila.data.add_language')
def test_add_language(add_language):
    dila.application.add_language('Polish', 'pl')
    assert add_language.mock_calls == [
        mock.call(
            'Polish', 'pl',
        )]


@mock.patch('dila.data.get_languages')
def test_get_resources(get_languages):
    get_languages.return_value = ['data_result']
    result = application.get_languages()
    get_languages.assert_called_with()
    assert result == ['data_result']


@mock.patch('dila.data.get_languages')
def test_get_languages_evaluates_iterator(get_languages):
    get_languages.return_value = itertools.repeat(0, 0)
    result = application.get_languages()
    assert result == []


@mock.patch('dila.data.get_language')
def test_get_language(get_language):
    get_language.return_value = 'Polski'
    result = application.get_language('pl')
    get_language.assert_called_with('pl')
    assert result == 'Polski'


@mock.patch('dila.data.get_resource')
def test_get_translated_string(get_resource):
    get_resource.return_value = 'data_result'
    result = application.get_resource('pl', '32')
    get_resource.assert_called_with('pl', '32')
    assert result == 'data_result'


@mock.patch('dila.data.delete_old_strings', mock.MagicMock())
@mock.patch('dila.data.add_or_update_base_string')
@mock.patch('dila.data.set_translated_string')
@mock.patch('dila.data.update_po_metadata')
def test_upload_po_file_with_translations(update_po_metadata, set_translated_string, add_or_update_base_string):
    add_or_update_base_string.return_value = 'string_pk'
    application.upload_po_file('1', test_po, translated_language_code='pl')
    assert add_or_update_base_string.mock_calls == [
        mock.call(
            '1',
            'Yellow',
            context='Disambiguation for context',
            comment='Programmer comment',
        )]
    assert set_translated_string.mock_calls == [
        mock.call(
            'pl',
            'string_pk',
            translation='Żółć',
            translator_comment='My comment',
        )]
    assert update_po_metadata.mock_calls == [
        mock.call('pl', '1', {'x': 'y'}),
    ]


@mock.patch('dila.data.delete_old_strings', mock.MagicMock())
@mock.patch('dila.data.update_po_metadata', mock.MagicMock())
@mock.patch('dila.data.add_or_update_base_string')
@mock.patch('dila.data.set_translated_string')
def test_upload_po_file_with_plural_translations(set_translated_string, add_or_update_base_string):
    add_or_update_base_string.return_value = 'string_pk'
    application.upload_po_file('1', test_plural_po, translated_language_code='pl')
    assert add_or_update_base_string.mock_calls == [
        mock.call(
            '1',
            '%d option',
            plural='%d options',
            context=None,
            comment='Programmer comment',
        )]
    assert set_translated_string.mock_calls == [
        mock.call(
            'pl',
            'string_pk',
            translation='%d opcję',
            translator_comment='',
            plural_translations=structures.PluralTranslations(
                few='%d opcje',
                many='%d opcji',
                other='%d opcji',
            )
        )]


@mock.patch('dila.data.delete_old_strings', mock.MagicMock())
@mock.patch('dila.data.add_or_update_base_string')
def test_upload_po_file_without_translations(add_or_update_base_string):
    application.upload_po_file('1', test_po)
    assert add_or_update_base_string.mock_calls == [
        mock.call(
            '1',
            'Yellow',
            context='Disambiguation for context',
            comment='Programmer comment',
        )]


@mock.patch('dila.data.delete_old_strings')
@mock.patch('dila.data.add_or_update_base_string')
def test_uploading_po_removes_old_strings(add_or_update_base_string, delete_old_strings):
    add_or_update_base_string.return_value = 'string_pk'
    application.upload_po_file('1', test_po)
    assert delete_old_strings.mock_calls == [
        mock.call(
            '1',
            keep_pks=['string_pk'],
        )]


@mock.patch('dila.data.get_translated_strings')
def test_get_translated_strings(get_translated_strings):
    get_translated_strings.return_value = 'data_result'
    result = application.get_translated_strings('pl', '1')
    get_translated_strings.assert_called_with('pl', '1')
    assert result == 'data_result'


@mock.patch('dila.data.get_translated_string')
def test_get_translated_string(get_translated_string):
    get_translated_string.return_value = 'data_result'
    result = application.get_translated_string('pl', '32')
    get_translated_string.assert_called_with('pl', '32')
    assert result == 'data_result'


@mock.patch('dila.data.set_translated_string')
def test_set_translated_strings(set_translated_string):
    application.set_translated_string('pl', '32', translation='x')
    set_translated_string.assert_called_with('pl', '32', translation='x')


@mock.patch('dila.data.get_translated_strings')
@mock.patch('dila.data.get_po_metadata')
def test_get_po_file(get_po_metadata, get_translated_strings):
    get_translated_strings.return_value = [
        structures.TranslatedStringData(
            pk='34',
            base_string='Yellow',
            plural='',
            translation='Żółć',
            comment='Programmer comment',
            translator_comment='My comment',
            context='Disambiguation for context',
            resource_pk='1',
            plural_translations=None,
        )
    ]
    get_po_metadata.return_value = {'x': 'y'}
    result = application.get_po_file('pl', '1')
    assert result == test_result_po


@mock.patch('dila.data.get_translated_strings')
@mock.patch('dila.data.get_po_metadata')
def test_get_po_file_with_plural_translations(get_po_metadata, get_translated_strings):
    get_translated_strings.return_value = [
        structures.TranslatedStringData(
            pk='34',
            base_string='%d option',
            plural='%d options',
            translation='%d opcję',
            comment='Programmer comment',
            translator_comment='',
            context='',
            resource_pk='1',
            plural_translations=structures.PluralTranslations(
                few='%d opcje',
                many='%d opcji',
                other='%d opcji',
            ),
        )
    ]
    get_po_metadata.return_value = {}
    result = application.get_po_file('pl', '1')
    assert result == test_result_plural_po


def test_authenticating_valid_user(config_ldap_setup):
    assert application.authenticate('shco01', 'bazinga')


def test_authenticating_user_without_password(config_ldap_setup):
    assert not application.authenticate('shco01', '')


def test_authenticating_invalid_user(config_ldap_setup):
    assert not application.authenticate('hacker', 'X" OR "a" = "A')
