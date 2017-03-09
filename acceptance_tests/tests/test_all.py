import pathlib
import urllib.request

import selenium.webdriver

PO_RESULT = '''#
msgid ""
msgstr ""

#. Programmer comment
msgctxt "Disambiguation for context"
msgid "One"
msgstr "New translation"
'''


def test_first(selenium: selenium.webdriver.Remote, running_server_url):
    open_homepage(running_server_url, selenium)
    upload_po(selenium)
    selenium.implicitly_wait(2)
    assert_translations_displayed(selenium)
    go_to_translation_editor(selenium)
    edit_translation(selenium)
    selenium.implicitly_wait(2)
    assert_new_translation_displayed(selenium)
    assert_download_link_works(selenium)


def open_homepage(running_server_url, selenium):
    selenium.get(running_server_url)
    assert selenium.title == 'Dila'


def upload_po(selenium):
    file_upload = selenium.find_element_by_css_selector('input[type="file"]')
    file_upload.clear()
    file_upload.send_keys(str(pathlib.Path(__file__).parent.parent / 'test.po'))
    selenium.find_element_by_css_selector('input[type="submit"]').click()


def assert_translations_displayed(selenium):
    content = selenium.find_element_by_tag_name('body').text
    assert 'File uploaded' in content
    assert 'Disambiguation for context' in content
    assert 'Een' in content


def go_to_translation_editor(selenium):
    selenium.find_element_by_link_text('One').click()


def edit_translation(selenium):
    text_input = selenium.find_element_by_css_selector('input[type="text"]')
    text_input.clear()
    text_input.send_keys('New translation')
    selenium.find_element_by_css_selector('input[type="submit"]').click()


def assert_new_translation_displayed(selenium):
    content = selenium.find_element_by_tag_name('body').text
    assert 'Translation changed' in content
    assert 'Disambiguation for context' in content
    assert 'New translation' in content


def assert_download_link_works(selenium):
    download_link = selenium.find_element_by_link_text('Download po')
    po_url = download_link.get_attribute('href')
    with urllib.request.urlopen(po_url) as new_po_file:
        new_po = new_po_file.read()
        assert new_po.decode('utf-8') == PO_RESULT
        assert new_po_file.info()['Content-Disposition'] == "attachment; filename=translations.po"
