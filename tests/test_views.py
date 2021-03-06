import io
import re
from unittest import mock

import flask
import pytest

from dila.application import structures
from dila.frontend.flask import user_tools

test_po = '''
# My comment
#. Programmer comment
#: location.c:23
#, fuzzy
msgctxt "Disambiguation for context"
msgid "Yellow"
msgstr "Żółć"
'''


@pytest.fixture
def authenticated_flask_client(flask_client):
    with flask_client.session_transaction() as session:
        user_tools.set_current_user(structures.User(
            authenticated=True,
            username='username',
            first_name='Sheldon',
            last_name='Cooper',
        ), session=session)
    return flask_client


def test_unauthenticated_home_redirects_to_login(flask_client):
    response = flask_client.get('/')
    assert response.status_code == 302
    assert response.location == 'http://localhost/login/'


@mock.patch('dila.application.get_resources')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_home(get_resources, authenticated_flask_client):
    get_resources.return_value = []
    response = authenticated_flask_client.get('/')
    assert '<title>Dila</title>' in response.data.decode()
    assert 'There are no resources.' in response.data.decode()
    assert 'There are no languages.' in response.data.decode()
    assert 'Sheldon Cooper' in response.data.decode()
    assert re.search('<li class="active">\s*<a class="navbar-brand" href="/">\s*Select resource\s*</a>\s*</li>',
                     response.data.decode())
    assert re.search('<form method="post" action="/logout/">\s+'
                     '<input type="submit" id="logout" class="[^"]+" value="Logout">\s+'
                     '</form>', response.data.decode())


@mock.patch('dila.application.get_resources')
@mock.patch('dila.application.get_languages')
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_home_with_selected_language_links_to_resource_page(get_languages, get_resources, authenticated_flask_client):
    get_resources.return_value = []
    get_languages.return_value = [
        structures.Language('polish', 'pl'),
        structures.Language('dutch', 'nl'),
    ]
    response = authenticated_flask_client.get('/lang/pl/')
    assert '<title>Dila</title>' in response.data.decode()
    assert 'There are no resources.' in response.data.decode()
    assert re.search('<li class="active">\s*<a class="navbar-brand" href="/lang/pl/">\s*Select resource\s*</a>\s*</li>',
                     response.data.decode())


@mock.patch('dila.application.get_resources')
@mock.patch('dila.application.get_languages')
def test_home_prompts_to_select_language(get_languages, get_resources, authenticated_flask_client):
    get_resources.return_value = []
    get_languages.return_value = [structures.Language('dutch', 'nl')]
    response = authenticated_flask_client.get('/')
    assert 'Select language.' in response.data.decode()



@mock.patch('dila.application.get_resources')
@mock.patch('dila.application.get_languages')
@mock.patch('dila.application.get_language')
def test_home_shows_selected_language(get_language, get_languages, get_resources, authenticated_flask_client):
    get_resources.return_value = []
    get_languages.return_value = [
        structures.Language('dutch', 'nl'),
    ]
    get_language.return_value = structures.Language('dutch', 'nl')
    response = authenticated_flask_client.get('/lang/nl/')
    assert 'Language: dutch.' in response.data.decode()


@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_add_resource_form_visible(authenticated_flask_client):
    response = authenticated_flask_client.get('/')
    assert re.search('<input class="[^"]*" id="new_resource_name" name="new_resource_name" type="text" value="">',
                     response.data.decode())
    assert re.search('<input id="add_new_resource" value="Add" type="submit">', response.data.decode())


@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_add_language_form_visible(authenticated_flask_client):
    response = authenticated_flask_client.get('/')
    assert re.search('<input class="[^"]*" id="new_language_name" name="new_language_name" type="text" value="">',
                     response.data.decode())
    assert re.search('<input class="[^"]*" id="new_language_short" name="new_language_short" type="text" value="">',
                     response.data.decode())
    assert re.search('<input id="add_new_language" value="Add" type="submit">', response.data.decode())


@mock.patch('dila.application.get_resources')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_links_to_resource_page(get_resources, authenticated_flask_client):
    get_resources.return_value = [
        structures.Resource(
            '34',
            'nice_language'
        )
    ]
    response = authenticated_flask_client.get('/')
    assert re.search('<a href="/res/34/">\s*nice_language\s*</a>', response.data.decode())

@mock.patch('dila.application.get_resources')
@mock.patch('dila.application.get_languages')
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_home_with_selected_language_links_to_resource_page(get_languages, get_resources, authenticated_flask_client):
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
    response = authenticated_flask_client.get('/lang/pl/')
    assert re.search('<a href="/lang/pl/res/34/">\s*nice_language\s*</a>', response.data.decode())

@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
@mock.patch('dila.application.add_resource')
def test_add_resource(add_resource, authenticated_flask_client):
    response = authenticated_flask_client.post(
        '/',
        data={
            'new_resource_name': 'new',
        }
    )
    assert response.status_code == 302
    response = authenticated_flask_client.get(response.location)
    assert 'Resource created' in response.data.decode()
    add_resource.assert_called_with('new')


@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
@mock.patch('dila.application.get_languages')
def test_home_links_to_language(get_languages, authenticated_flask_client):
    get_languages.return_value = [
        structures.Language('polish', 'pl')
    ]
    response = authenticated_flask_client.get('/')
    assert re.search('<a class="[^"]*" href="/lang/pl/">\s*polish\s*</a>', response.data.decode())


@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
@mock.patch('dila.application.get_languages')
def test_home_with_selected_language_links_to_language(get_languages, authenticated_flask_client):
    get_languages.return_value = [
        structures.Language('polish', 'pl'),
        structures.Language('dutch', 'nl'),
    ]
    response = authenticated_flask_client.get('/lang/pl/')
    assert re.search('<a class="[^"]*" href="/lang/nl/">\s*dutch\s*</a>', response.data.decode())


@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
@mock.patch('dila.application.add_language')
def test_add_language(add_language, authenticated_flask_client):
    response = authenticated_flask_client.post(
        '/add-language/',
        data={
            'new_language_name': 'polish',
            'new_language_short': 'pl',
            'next': '/',
        }
    )
    assert response.status_code == 302
    assert response.location == 'http://localhost/lang/pl/'
    response = authenticated_flask_client.get(response.location)
    assert 'Language added' in response.data.decode()
    add_language.assert_called_with('polish', 'pl')


@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_resource_page(authenticated_flask_client):
    response = authenticated_flask_client.get('/res/1/')
    assert re.search('<li class="">\s*<a class="navbar-brand" href="/">\s*Select resource\s*</a>\s*</li>',
                     response.data.decode())


@mock.patch('dila.application.get_translated_strings')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_resource_page_with_selected_language(get_translated_strings, authenticated_flask_client):
    response = authenticated_flask_client.get('/lang/pl/res/1/')
    assert re.search('<li class="">\s*<a class="navbar-brand" href="/lang/pl/">\s*Select resource\s*</a>\s*</li>',
                     response.data.decode())
    get_translated_strings.assert_called_with('pl', '1')


@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
@mock.patch('dila.application.get_languages')
def test_resource_page_links_to_language(get_languages, authenticated_flask_client):
    get_languages.return_value = [
        structures.Language('polish', 'pl')
    ]
    response = authenticated_flask_client.get('/res/1/')
    assert re.search('<a class="[^"]*" href="/lang/pl/res/1/">\s*polish\s*</a>', response.data.decode())


@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
@mock.patch('dila.application.get_languages')
def test_resource_page_with_selected_language_links_to_language(get_languages, authenticated_flask_client):
    get_languages.return_value = [
        structures.Language('polish', 'pl'),
        structures.Language('dutch', 'nl'),
    ]
    response = authenticated_flask_client.get('/lang/pl/res/1/')
    assert re.search('<a class="[^"]*" href="/lang/nl/res/1/">\s*dutch\s*</a>', response.data.decode())


@mock.patch('dila.application.get_resources', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
@mock.patch('dila.application.get_languages')
def test_resource_page_ensures_language_is_selected(get_languages, authenticated_flask_client):
    get_languages.return_value = [
        structures.Language('polish', 'pl')
    ]
    response = authenticated_flask_client.get('/res/1/')
    assert 'Select language' in response.data.decode()


@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.upload_po_file', mock.MagicMock())
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_upload_po_file_form_visible(authenticated_flask_client):
    response = authenticated_flask_client.get('/lang/pl/res/1/')
    assert '<input id="po_file" name="po_file" type="file">' in response.data.decode()
    assert '<input id="apply_translations" name="apply_translations" type="checkbox" value="y">' in response.data.decode()

@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.upload_po_file', mock.MagicMock())
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_download_po_file_visible(authenticated_flask_client):
    response = authenticated_flask_client.get('/lang/pl/res/1/')
    assert re.search('<a class="[^"]*" href="/lang/pl/res/1/po-file/">\s*Download po\s*</a>', response.data.decode())


@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.upload_po_file')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_upload_po_file(upload_po_file, authenticated_flask_client):
    response = authenticated_flask_client.post(
        '/lang/pl/res/1/',
        data={
            'po_file': (io.BytesIO(test_po.encode()), 'test.po'),
            'apply_translations': 'y',
        }
    )
    assert response.status_code == 302
    assert response.location == 'http://localhost/lang/pl/res/1/'
    response = authenticated_flask_client.get(response.location)
    assert 'File uploaded' in response.data.decode()
    upload_po_file.assert_called_with('1', test_po, translated_language_code='pl')


@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.upload_po_file')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_upload_po_file_without_translations(upload_po_file, authenticated_flask_client):
    response = authenticated_flask_client.post(
        '/lang/pl/res/1/',
        data={
            'po_file': (io.BytesIO(test_po.encode()), 'test.po'),
        }
    )
    upload_po_file.assert_called_with('1', test_po)


@mock.patch('dila.application.get_translated_strings')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_links_to_stored_translation_page(get_translated_strings, authenticated_flask_client):
    get_translated_strings.return_value = [
        structures.TranslatedStringData(
            pk='34',
            base_string='base_string',
            plural='',
            translation='translation',
            comment='comment',
            translator_comment='translator_comment',
            context='context',
            resource_pk='1',
            plural_translations=None,
        )
    ]
    response = authenticated_flask_client.get('/lang/pl/res/1/')
    assert re.search('<a href="/lang/pl/edit/34/">\s*base_string\s*</a>', response.data.decode())

@mock.patch('dila.application.get_translated_string')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_get_translation_form(get_translated_string, authenticated_flask_client):
    get_translated_string.return_value = structures.TranslatedStringData(
        pk='34',
        base_string='base_string',
        plural='',
        translation='translation-x',
        comment='comment',
        translator_comment='translator_comment',
        context='context',
        resource_pk='1',
        plural_translations=None,
    )
    response = authenticated_flask_client.get('/lang/pl/edit/34/')
    assert re.search('<textarea class="[^"]*" cols="[^"]*" id="translation" name="translation" rows="[^"]*">'
                     'translation-x</textarea>', response.data.decode())
    assert re.search('<textarea class="[^"]*" cols="[^"]*" id="translator_comment" name="translator_comment" '
                     'rows="[^"]*">translator_comment</textarea>', response.data.decode())
    assert 'action="/lang/pl/edit/34/"' in response.data.decode()


@mock.patch('dila.application.get_translated_string')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_get_plural_translation_form(get_translated_string, authenticated_flask_client):
    get_translated_string.return_value = structures.TranslatedStringData(
        pk='34',
        base_string='%d option',
        plural='%d options',
        translation='%d opcja',
        comment='comment',
        translator_comment='translator_comment',
        context='context',
        resource_pk='1',
        plural_translations=structures.PluralTranslations(
            few='%d opcje',
            many='%d opcji',
            other='%d opcji',
        ),
    )
    response = authenticated_flask_client.get('/lang/pl/edit/34/')
    assert re.search('<textarea class="[^"]*" cols="[^"]*" id="translation_one" name="translation_one" rows="[^"]*">'
                     '%d opcja</textarea>', response.data.decode())
    assert re.search('<textarea class="[^"]*" cols="[^"]*" id="translation_few" name="translation_few" rows="[^"]*">'
                     '%d opcje</textarea>', response.data.decode())
    assert re.search('<textarea class="[^"]*" cols="[^"]*" id="translation_many" name="translation_many" rows="[^"]*">'
                     '%d opcji</textarea>', response.data.decode())
    assert re.search('<textarea class="[^"]*" cols="[^"]*" id="translation_other" name="translation_other" rows="[^"]*">'
                     '%d opcji</textarea>', response.data.decode())
    assert re.search('<textarea class="[^"]*" cols="[^"]*" id="translator_comment" name="translator_comment" '
                     'rows="[^"]*">translator_comment</textarea>', response.data.decode())
    assert 'action="/lang/pl/edit/34/"' in response.data.decode()


@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.get_translated_string')
@mock.patch('dila.application.set_translated_string')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_post_translation_form(set_translated_string, get_translated_string, authenticated_flask_client):
    get_translated_string.return_value = structures.TranslatedStringData(
        pk='34',
        base_string='base_string',
        plural='',
        translation='translation-x',
        comment='comment',
        translator_comment='translator_comment',
        context='context',
        resource_pk='1',
        plural_translations=None,
    )
    response = authenticated_flask_client.post('/lang/pl/edit/34/', data={
        'translation': 'new-translation',
        'translator_comment': 'new-translator-comment',
    })
    assert response.status_code == 302
    assert response.location == 'http://localhost/lang/pl/res/1/'
    response = authenticated_flask_client.get(response.location)
    assert 'Translation changed' in response.data.decode()
    set_translated_string.assert_called_with('pl', '34', translation='new-translation',
                                             translator_comment='new-translator-comment')

@mock.patch('dila.application.get_translated_strings', mock.MagicMock())
@mock.patch('dila.application.get_translated_string')
@mock.patch('dila.application.set_translated_string')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_post_plural_translation_form(set_translated_string, get_translated_string, authenticated_flask_client):
    get_translated_string.return_value = structures.TranslatedStringData(
        pk='34',
        base_string='%d option',
        plural='%d options',
        translation='%d alternatywa',
        comment='comment',
        translator_comment='translator_comment',
        context='context',
        resource_pk='1',
        plural_translations=structures.PluralTranslations(
            few='%d alternatywy',
            many='%d alternatyw',
            other='%d alternatyw',
        ),
    )
    response = authenticated_flask_client.post('/lang/pl/edit/34/', data={
        'translation_one': '%d opcja',
        'translation_few': '%d opcje',
        'translation_many': '%d opcji',
        'translation_other': '%d opcji',
        'translator_comment': 'new-translator-comment',
    })
    assert response.status_code == 302
    assert response.location == 'http://localhost/lang/pl/res/1/'
    response = authenticated_flask_client.get(response.location)
    assert 'Translation changed' in response.data.decode()
    set_translated_string.assert_called_with('pl', '34', translation='%d opcja',
                                             translator_comment='new-translator-comment',
                                             plural_translations=structures.PluralTranslations(
                                                 few='%d opcje',
                                                 many='%d opcji',
                                                 other='%d opcji',
                                             ))


@mock.patch('dila.application.get_po_file')
@mock.patch('dila.application.get_languages', mock.MagicMock())
@mock.patch('dila.application.get_language', mock.MagicMock())
def test_get_po_file_view(get_po_file, authenticated_flask_client):
    get_po_file.return_value = 'asdf'
    response = authenticated_flask_client.get('/lang/pl/res/1/po-file/')
    assert 'asdf' == response.data.decode()
    assert "attachment; filename=translations.po" == response.headers["Content-Disposition"]
