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


@mock.patch('dila.application.get_resources')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_home(get_resources, flask_client):
    get_resources.return_value = []
    response = flask_client.get('/')
    assert '<title>Dila</title>' in response.data.decode()
    assert 'There are no resources.' in response.data.decode()
    assert 'There are no languages.' in response.data.decode()
    assert re.search('<li class="active">\s*<a class="navbar-brand" href="/">\s*Select resource\s*</a>\s*</li>',
                     response.data.decode())


@mock.patch('dila.application.get_resources')
@mock.patch('dila.application.get_languages')
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_home_with_selected_language_links_to_resource_page(get_languages, get_resources, flask_client):
    get_resources.return_value = []
    get_languages.return_value = [
        structures.Language('polish', 'pl'),
        structures.Language('dutch', 'nl'),
    ]
    response = flask_client.get('/lang/pl/')
    assert '<title>Dila</title>' in response.data.decode()
    assert 'There are no resources.' in response.data.decode()
    assert re.search('<li class="active">\s*<a class="navbar-brand" href="/lang/pl/">\s*Select resource\s*</a>\s*</li>',
                     response.data.decode())


@mock.patch('dila.application.get_resources')
@mock.patch('dila.application.get_languages')
def test_home_prompts_to_select_language(get_languages, get_resources, flask_client):
    get_resources.return_value = []
    get_languages.return_value = [structures.Language('dutch', 'nl')]
    response = flask_client.get('/')
    assert 'Select language.' in response.data.decode()



@mock.patch('dila.application.get_resources')
@mock.patch('dila.application.get_languages')
@mock.patch('dila.application.get_language')
def test_home_shows_selected_language(get_language, get_languages, get_resources, flask_client):
    get_resources.return_value = []
    get_languages.return_value = [
        structures.Language('dutch', 'nl'),
    ]
    get_language.return_value = structures.Language('dutch', 'nl')
    response = flask_client.get('/lang/nl/')
    assert 'Language: dutch.' in response.data.decode()


@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_add_resource_form_visible(flask_client):
    response = flask_client.get('/')
    assert re.search('<input class="[^"]*" id="new_resource_name" name="new_resource_name" type="text" value="">',
                     response.data.decode())
    assert re.search('<input id="add_new_resource" value="Add" type="submit">', response.data.decode())


@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_add_language_form_visible(flask_client):
    response = flask_client.get('/')
    assert re.search('<input class="[^"]*" id="new_language_name" name="new_language_name" type="text" value="">',
                     response.data.decode())
    assert re.search('<input class="[^"]*" id="new_language_short" name="new_language_short" type="text" value="">',
                     response.data.decode())
    assert re.search('<input id="add_new_language" value="Add" type="submit">', response.data.decode())


@mock.patch('dila.application.get_resources')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_links_to_resource_page(get_resources, flask_client):
    get_resources.return_value = [
        structures.Resource(
            '34',
            'nice_language'
        )
    ]
    response = flask_client.get('/')
    assert re.search('<a href="/res/34/">\s*nice_language\s*</a>', response.data.decode())

@mock.patch('dila.application.get_resources')
@mock.patch('dila.application.get_languages')
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_home_with_selected_language_links_to_resource_page(get_languages, get_resources, flask_client):
    get_languages.return_value = [
        structures.Language('polish', 'pl'),
        structures.Language('dutch', 'nl'),
    ]
    get_resources.return_value = [
        structures.Resource(
            '34',
            'nice_language'
        )
    ]
    response = flask_client.get('/lang/pl/')
    assert re.search('<a href="/lang/pl/res/34/">\s*nice_language\s*</a>', response.data.decode())

@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
@mock.patch('dila.application.add_resource')
def test_add_resource(add_resource, flask_client):
    response = flask_client.post(
        '/',
        data={
            'new_resource_name': 'new',
        }
    )
    assert response.status_code == 302
    response = flask_client.get(response.location)
    assert 'Resource created' in response.data.decode()
    add_resource.assert_called_with('new')


@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
@mock.patch('dila.application.get_languages')
def test_home_links_to_language(get_languages, flask_client):
    get_languages.return_value = [
        structures.Language('polish', 'pl')
    ]
    response = flask_client.get('/')
    assert re.search('<a href="/lang/pl/">\s*polish\s*</a>', response.data.decode())


@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
@mock.patch('dila.application.get_languages')
def test_home_with_selected_language_links_to_language(get_languages, flask_client):
    get_languages.return_value = [
        structures.Language('polish', 'pl'),
        structures.Language('dutch', 'nl'),
    ]
    response = flask_client.get('/lang/pl/')
    assert re.search('<a href="/lang/nl/">\s*dutch\s*</a>', response.data.decode())


@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
@mock.patch('dila.application.add_language')
def test_add_language(add_language, flask_client):
    response = flask_client.post(
        '/add-language/',
        data={
            'new_language_name': 'polish',
            'new_language_short': 'pl',
            'next': '/',
        }
    )
    assert response.status_code == 302
    response = flask_client.get(response.location)
    assert 'Language added' in response.data.decode()
    add_language.assert_called_with('polish', 'pl')


@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_resource_page(flask_client):
    response = flask_client.get('/res/1/')
    assert re.search('<li class="">\s*<a class="navbar-brand" href="/">\s*Select resource\s*</a>\s*</li>',
                     response.data.decode())


@mock.patch('dila.application.get_translated_strings')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_resource_page_with_selected_language(get_translated_strings, flask_client):
    response = flask_client.get('/lang/pl/res/1/')
    assert re.search('<li class="">\s*<a class="navbar-brand" href="/lang/pl/">\s*Select resource\s*</a>\s*</li>',
                     response.data.decode())
    get_translated_strings.assert_called_with('pl', '1')


@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
@mock.patch('dila.application.get_languages')
def test_resource_page_links_to_language(get_languages, flask_client):
    get_languages.return_value = [
        structures.Language('polish', 'pl')
    ]
    response = flask_client.get('/res/1/')
    assert re.search('<a href="/lang/pl/res/1/">\s*polish\s*</a>', response.data.decode())


@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
@mock.patch('dila.application.get_languages')
def test_resource_page_with_selected_language_links_to_language(get_languages, flask_client):
    get_languages.return_value = [
        structures.Language('polish', 'pl'),
        structures.Language('dutch', 'nl'),
    ]
    response = flask_client.get('/lang/pl/res/1/')
    assert re.search('<a href="/lang/nl/res/1/">\s*dutch\s*</a>', response.data.decode())


@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
@mock.patch('dila.application.get_languages')
def test_resource_page_ensures_language_is_selected(get_languages, flask_client):
    get_languages.return_value = [
        structures.Language('polish', 'pl')
    ]
    response = flask_client.get('/res/1/')
    assert 'Select language' in response.data.decode()


@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.upload_po_file', mock.MagicMock())
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_upload_po_file_form_visible(flask_client):
    response = flask_client.get('/lang/pl/res/1/')
    assert '<input id="po_file" name="po_file" type="file">' in response.data.decode()

@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.upload_po_file', mock.MagicMock())
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_download_po_file_visible(flask_client):
    response = flask_client.get('/lang/pl/res/1/')
    assert re.search('<a class="[^"]*" href="/lang/pl/res/1/po-file/">\s*Download po\s*</a>', response.data.decode())


@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.upload_po_file')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_upload_po_file(upload_po_file, flask_client):
    response = flask_client.post(
        '/lang/pl/res/1/',
        data={
            'po_file': (io.BytesIO(test_po.encode()), 'test.po'),
        }
    )
    assert response.status_code == 302
    response = flask_client.get(response.location)
    assert 'File uploaded' in response.data.decode()
    upload_po_file.assert_called_with('1', test_po, translated_language_code='pl')


@mock.patch('dila.application.get_translated_strings')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_links_to_stored_translation_page(get_translated_strings, flask_client):
    get_translated_strings.return_value = [
        structures.TranslatedStringData(
            '34',
            'base_string',
            'translation',
            'comment',
            'translator_comment',
            'context',
            '1',
        )
    ]
    response = flask_client.get('/lang/pl/res/1/')
    assert re.search('<a href="/lang/pl/edit/34/">\s*base_string\s*</a>', response.data.decode())

@mock.patch('dila.application.get_translated_string')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_get_translation_form(get_translated_string, flask_client):
    get_translated_string.return_value = structures.TranslatedStringData(
        '34',
        'base_string',
        'translation-x',
        'comment',
        'translator_comment',
        'context',
        '1',
    )
    response = flask_client.get('/lang/pl/edit/34/')
    assert re.search('<input class="[^"]*" id="translation" name="translation" type="text" value="translation-x">',
                     response.data.decode())
    assert 'action="/lang/pl/edit/34/"' in response.data.decode()


@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.get_translated_string')
@mock.patch('dila.application.set_translated_string')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_post_translation_form(set_translated_string, get_translated_string, flask_client):
    get_translated_string.return_value = structures.TranslatedStringData(
        '34',
        'base_string',
        'translation-x',
        'comment',
        'translator_comment',
        'context',
        '1',
    )
    response = flask_client.post('/lang/pl/edit/34/', data={'translation': 'new-translation'})
    assert response.status_code == 302
    assert response.location == 'http://localhost/lang/pl/res/1/'
    response = flask_client.get(response.location)
    assert 'Translation changed' in response.data.decode()
    set_translated_string.assert_called_with('pl', '34', translation='new-translation')


@mock.patch('dila.application.get_po_file')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_get_po_file_view(get_po_file, flask_client):
    get_po_file.return_value = 'asdf'
    response = flask_client.get('/lang/pl/res/1/po-file/')
    assert 'asdf' == response.data.decode()
    assert "attachment; filename=translations.po" == response.headers["Content-Disposition"]
