from unittest import mock

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


@mock.patch('dila.data.add_translated_string')
def test_upload_translated_po_file_with(add_translated_string):
    application.upload_translated_po_file(test_po)
    assert add_translated_string.mock_calls == [
        mock.call(
            'Yellow',
            context='Disambiguation for context',
            translation='Żółć',
            comment='Programmer comment',
            translator_comment='',
        )]


@mock.patch('dila.data.get_translated_strings')
def test_get_translated_strings(get_translated_strings):
    get_translated_strings.return_value = 'data_result'
    result = application.get_translated_strings()
    get_translated_strings.assert_called_with()
    assert result == 'data_result'
