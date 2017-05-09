import pathlib
import urllib.request

import pytest
import selenium.webdriver
import time

PO_RESULT = '''#
msgid ""
msgstr ""

#. Programmer comment
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
    assert_no_resources_info(selenium)
    add_resource(selenium, 'first resource')
    time.sleep(1)
    add_resource(selenium, 'second resource')
    time.sleep(1)
    select_resource(selenium, 'first resource')
    assert_no_language_info(selenium)
    add_language(selenium, 'dutch', 'nl')
    time.sleep(1)
    add_language(selenium, 'polish', 'pl')
    time.sleep(1)
    assert_language_selected(selenium, 'polish')
    pytest.fail()
    select_language(selenium, 'dutch')
    assert_language_selected(selenium, 'dutch')
    upload_po(selenium, 'test.po', with_translations=True)
    time.sleep(1)
    assert_translations_displayed(selenium)
    go_to_translation_editor(selenium)
    edit_translation(selenium)
    time.sleep(1)
    assert_new_translation_displayed(selenium)
    upload_po(selenium, 'new_untranslated.po')
    assert_changed_translation_strings(selenium)
    assert_download_link_works(selenium)
    go_homepage(selenium)
    select_resource(selenium, 'second resource')
    time.sleep(1)
    assert_no_translations_displayed(selenium)
    go_homepage(selenium)
    select_resource(selenium, 'first resource')
    select_language(selenium, 'polish')
    time.sleep(1)
    assert_strings_without_translations_displayed(selenium)


def open_homepage(running_server_url, selenium):
    selenium.get(running_server_url)
    assert selenium.title == 'Dila'


def assert_no_resources_info(selenium):
    content = selenium.find_element_by_tag_name('body').text
    assert 'There are no resources.' in content


def add_resource(selenium, name):
    selenium.find_element_by_id('addResourceButton').click()
    time.sleep(1)
    resource_name = selenium.find_element_by_id('new_resource_name')
    resource_name.clear()
    resource_name.send_keys(name)
    selenium.find_element_by_id('add_new_resource').click()


def select_resource(selenium, name):
    selenium.find_element_by_link_text(name).click()


def assert_no_language_info(selenium):
    content = selenium.find_element_by_tag_name('body').text
    assert 'There are no languages.' in content


def add_language(selenium, name, short):
    selenium.find_element_by_id('languageMenuButton').click()
    selenium.find_element_by_id('addLanguageButton').click()
    time.sleep(1)
    resource_name = selenium.find_element_by_id('new_language_name')
    resource_name.clear()
    resource_name.send_keys(name)
    language_short = selenium.find_element_by_id('new_language_short')
    language_short.clear()
    language_short.send_keys(short)
    selenium.find_element_by_id('add_new_language').click()


def select_language(selenium, name):
    selenium.find_element_by_link_text(name).click()


def assert_language_selected(selenium, name):
    content = selenium.find_element_by_tag_name('body').text
    assert 'Current language: {}.'.format(name) in content


def go_homepage(selenium):
    selenium.find_element_by_link_text('Select resource').click()


def upload_po(selenium, filename, with_translations=False):
    file_upload = selenium.find_element_by_id('po_file')
    file_upload.clear()
    file_upload.send_keys(str(pathlib.Path(__file__).parent.parent / filename))
    if with_translations:
        selenium.find_element_by_id('apply_translations').click()
    selenium.find_element_by_id('upload_po_file').click()


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
    assert 'Een' in content
    assert 'Disambiguation for second context' not in content
    assert 'Twee' not in content
    assert 'Disambiguation for third context' in content

def assert_download_link_works(selenium):
    download_link = selenium.find_element_by_link_text('Download po')
    po_url = download_link.get_attribute('href')
    with urllib.request.urlopen(po_url) as new_po_file:
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
