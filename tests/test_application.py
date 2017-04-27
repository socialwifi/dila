from unittest import mock

from dila.application import structures

from dila import application

test_po = '''
# My comment
#. Programmer comment
#: location.c:23
#, fuzzy
msgctxt "Disambiguation for context"
msgid "Yellow"
msgstr "Żółć"
'''

test_result_po = '''#
msgid ""
msgstr ""

#. Programmer comment
# My comment
msgctxt "Disambiguation for context"
msgid "Yellow"
msgstr "Żółć"
'''


@mock.patch('dila.data.add_translated_string')
def test_upload_translated_po_file_with(add_translated_string):
    application.upload_translated_po_file('1', test_po)
    assert add_translated_string.mock_calls == [
        mock.call(
            '1',
            'Yellow',
            context='Disambiguation for context',
            translation='Żółć',
            comment='Programmer comment',
            translator_comment='',
        )]
    application.upload_translated_po_file('1', test_po)


@mock.patch('dila.data.get_translated_strings')
def test_get_translated_strings(get_translated_strings):
    get_translated_strings.return_value = 'data_result'
    result = application.get_translated_strings('1')
    get_translated_strings.assert_called_with('1')
    assert result == 'data_result'


@mock.patch('dila.data.get_translated_string')
def test_get_translated_strings(get_translated_string):
    get_translated_string.return_value = 'data_result'
    result = application.get_translated_string('1', '32')
    get_translated_string.assert_called_with('1', '32')
    assert result == 'data_result'


@mock.patch('dila.data.set_translated_string')
def test_set_translated_strings(set_translated_string):
    application.set_translated_string('1', '32', translation='x')
    set_translated_string.assert_called_with('1', '32', translation='x')


@mock.patch('dila.data.get_translated_strings')
def test_get_po_file(get_translated_strings):
    get_translated_strings.return_value = [
        structures.TranslatedStringData(
            '34',
            'Yellow',
            'Żółć',
            'Programmer comment',
            'My comment',
            'Disambiguation for context',
        )
    ]
    result = application.get_po_file('1')
    assert result == test_result_po
