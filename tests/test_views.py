import io
import re
from unittest import mock

from dila.application import structures

test_po = '''
# My comment
#. Programmer comment
#: location.c:23
#, fuzzy
msgctxt "Disambiguation for context"
msgid "Yellow"
msgstr "Żółć"
'''


@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
def test_home(flask_client):
    response = flask_client.get('/')
    assert '<title>Dila</title>' in response.data.decode()


@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.upload_translated_po_file', mock.MagicMock())
def test_upload_po_file_form_visible(flask_client):
    response = flask_client.get('/')
    assert '<input id="po_file" name="po_file" type="file">' in response.data.decode()


@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.upload_translated_po_file')
def test_upload_po_file(upload_translated_po_file, flask_client):
    response = flask_client.post(
        '/',
        data={
            'po_file': (io.BytesIO(test_po.encode()), 'test.po'),
        }
    )
    assert response.status_code == 302
    response = flask_client.get(response.location)
    assert 'File uploaded' in response.data.decode()
    upload_translated_po_file.assert_called_with(test_po)


@mock.patch('dila.application.get_translated_strings')
def test_links_to_stored_translation_page(get_translated_strings, flask_client):
    get_translated_strings.return_value = [
        structures.TranslatedStringData(
            '34',
            'base_string',
            'translation',
            'comment',
            'translator_comment',
            'context',
        )
    ]
    response = flask_client.get('/')
    assert re.search('<a href="/edit/34/">\s+base_string\s+</a>', response.data.decode())

@mock.patch('dila.application.get_translated_string')
def test_get_translation_form(get_translated_string, flask_client):
    get_translated_string.return_value = structures.TranslatedStringData(
        '34',
        'base_string',
        'translation-x',
        'comment',
        'translator_comment',
        'context',
    )
    response = flask_client.get('/edit/34/')
    assert re.search('<input id="translation" name="translation" type="text" value="translation-x">',
                     response.data.decode())


@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.get_translated_string')
@mock.patch('dila.application.set_translated_string')
def test_post_translation_form(set_translated_string, get_translated_string, flask_client):
    get_translated_string.return_value = structures.TranslatedStringData(
        '34',
        'base_string',
        'translation-x',
        'comment',
        'translator_comment',
        'context',
    )
    response = flask_client.post('/edit/34/', data={'translation': 'new-translation'})
    assert response.status_code == 302
    response = flask_client.get(response.location)
    assert 'Translation changed' in response.data.decode()
    set_translated_string.assert_called_with('34', translation='new-translation')
