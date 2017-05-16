import pathlib
import urllib.request

import pytest
import selenium.webdriver
import selenium.common.exceptions
import tenacity
import time

PO_RESULT = '''#
msgid ""
msgstr ""
"Language: nl\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\\n"

#. Programmer comment
# My comment
msgctxt "Disambiguation for context"
msgid "One"
msgstr "New translation"

#. Programmer third comment
msgctxt "Disambiguation for third context"
msgid "Three"
msgstr ""
'''


def test_first(selenium: selenium.webdriver.Remote, running_server_url):
    open_homepage(running_server_url, selenium)
    login(selenium, 'admin', 'admin')
    retry_selenium(assert_logged_in)(selenium, 'Super Admin')
    assert_no_resources_info(selenium)
    add_resource(selenium, 'first resource')
    retry_selenium(add_resource)(selenium, 'second resource')
    retry_selenium(select_resource)(selenium, 'first resource')
    time.sleep(0.1)
    retry_selenium(assert_no_language_info)(selenium)
    add_language(selenium, 'dutch', 'nl')
    retry_selenium(add_language)(selenium, 'polish', 'pl')
    retry_selenium(assert_language_selected)(selenium, 'polish')
    select_language(selenium, 'dutch')
    retry_selenium(assert_language_selected)(selenium, 'dutch')
    upload_po(selenium, 'test.po', with_translations=True)
    retry_selenium(assert_translations_displayed)(selenium)
    go_to_translation_editor(selenium)
    edit_translation(selenium)
    retry_selenium(assert_new_translation_displayed)(selenium)
    upload_po(selenium, 'new_untranslated.po')
    retry_selenium(assert_changed_translation_strings)(selenium)
    assert_download_link_works(selenium)
    go_homepage(selenium)
    retry_selenium(select_resource)(selenium, 'second resource')
    retry_selenium(assert_no_translations_displayed)(selenium)
    go_homepage(selenium)
    retry_selenium(select_resource)(selenium, 'first resource')
    retry_selenium(select_language)(selenium, 'polish')
    retry_selenium(assert_strings_without_translations_displayed)(selenium)
    logout(selenium)


retry_selenium = tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=0.25),
    retry=tenacity.retry_if_exception_type((
        selenium.common.exceptions.StaleElementReferenceException,
        selenium.common.exceptions.ElementNotVisibleException,
        selenium.common.exceptions.InvalidElementStateException,
        selenium.common.exceptions.NoSuchElementException,
        AssertionError,
    )),
    reraise=True,
)


def open_homepage(running_server_url, selenium):
    selenium.get(running_server_url)
    assert selenium.title == 'Dila'


def login(selenium, username, password):
    username_field = selenium.find_element_by_id('username')
    username_field.clear()
    username_field.send_keys(username)
    password_field = selenium.find_element_by_id('password')
    password_field.clear()
    password_field.send_keys(password)
    selenium.find_element_by_id('login').click()


def assert_logged_in(selenium, display_name):
    content = selenium.find_element_by_id('userMenu').text
    assert display_name in content


def assert_no_resources_info(selenium):
    content = selenium.find_element_by_tag_name('body').text
    assert 'There are no resources.' in content


def add_resource(selenium, name):
    @retry_selenium
    def open_add_resource_menu():
        selenium.find_element_by_id('addResourceButton').click()
    open_add_resource_menu()

    @retry_selenium
    def try_add_resource():
        resource_name = selenium.find_element_by_id('new_resource_name')
        resource_name.clear()
        resource_name.send_keys(name)
        selenium.find_element_by_id('add_new_resource').click()
    try_add_resource()


def select_resource(selenium, name):
    selenium.find_element_by_link_text(name).click()


def assert_no_language_info(selenium):
    content = selenium.find_element_by_tag_name('body').text
    assert 'There are no languages.' in content


def add_language(selenium, name, short):
    @retry_selenium
    def open_add_language_menu():
        selenium.find_element_by_id('languageMenuButton').click()
        selenium.find_element_by_id('addLanguageButton').click()
    open_add_language_menu()

    @retry_selenium
    def try_add_language():
        resource_name = selenium.find_element_by_id('new_language_name')
        resource_name.clear()
        resource_name.send_keys(name)
        language_short = selenium.find_element_by_id('new_language_short')
        language_short.clear()
        language_short.send_keys(short)
        selenium.find_element_by_id('add_new_language').click()
    try_add_language()


def select_language(selenium, name):
    selenium.find_element_by_id('languageMenuButton').click()
    selenium.find_element_by_link_text(name).click()


def assert_language_selected(selenium, name):
    content = selenium.find_element_by_tag_name('body').text
    assert 'Language: {}.'.format(name) in content


def go_homepage(selenium):
    selenium.find_element_by_link_text('Select resource').click()


def upload_po(selenium, filename, with_translations=False):
    @retry_selenium
    def open_po_menu():
        selenium.find_element_by_id('uploadPoFileButton').click()
    open_po_menu()

    @retry_selenium
    def try_upload_po():
        file_upload = selenium.find_element_by_id('po_file')
        file_upload.clear()
        file_upload.send_keys(str(pathlib.Path(__file__).parent.parent / filename))
        if with_translations:
            selenium.find_element_by_id('apply_translations').click()
        selenium.find_element_by_id('upload_po_file').click()
    try_upload_po()


def assert_translations_displayed(selenium):
    content = selenium.find_element_by_tag_name('body').text
    assert 'File uploaded' in content
    assert 'Disambiguation for context' in content
    assert 'Een' in content
    assert 'Disambiguation for second context' in content
    assert 'Twee' in content


def go_to_translation_editor(selenium):
    selenium.find_element_by_link_text('One').click()


def edit_translation(selenium):
    text_input = selenium.find_element_by_id('translation')
    text_input.clear()
    text_input.send_keys('New translation')
    selenium.find_element_by_id('submit').click()


def assert_new_translation_displayed(selenium):
    content = selenium.find_element_by_tag_name('body').text
    assert 'Translation changed' in content
    assert 'Disambiguation for context' in content
    assert 'New translation' in content


def assert_changed_translation_strings(selenium):
    content = selenium.find_element_by_tag_name('body').text
    assert 'File uploaded' in content
    assert 'Disambiguation for context' in content
    assert 'New translation' in content
    assert 'Disambiguation for second context' not in content
    assert 'Twee' not in content
    assert 'Disambiguation for third context' in content


def assert_download_link_works(selenium):
    download_link = selenium.find_element_by_link_text('Download po')
    po_url = download_link.get_attribute('href')
    opener = urllib.request.URLopener()
    cookie_header = 'session={}'.format(selenium.get_cookie('session')['value'])
    print(cookie_header)
    opener.addheader('Cookie', cookie_header)
    with opener.open(po_url) as new_po_file:
        new_po = new_po_file.read()
        assert new_po.decode('utf-8') == PO_RESULT
        assert new_po_file.info()['Content-Disposition'] == "attachment; filename=translations.po"


def assert_no_translations_displayed(selenium):
    content = selenium.find_element_by_tag_name('body').text
    assert 'File uploaded' not in content
    assert 'Disambiguation for context' not in content
    assert 'New translation' not in content


def assert_strings_without_translations_displayed(selenium):
    content = selenium.find_element_by_tag_name('body').text
    assert 'Disambiguation for context' in content
    assert 'One' in content
    assert 'Een' not in content


def logout(selenium):
    @retry_selenium
    def open_add_language_menu():
        selenium.find_element_by_id('userMenuButton').click()
        selenium.find_element_by_id('logout').click()
    open_add_language_menu()

    @retry_selenium
    def assert_login_page():
        assert selenium.find_element_by_id('login')
    assert_login_page()
