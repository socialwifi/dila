import pathlib
import pytest
import selenium.webdriver


def test_first(selenium: selenium.webdriver.Remote, running_server_url):
    selenium.get(running_server_url)
    assert selenium.title == 'Dila'
    file_upload = selenium.find_element_by_css_selector('input[type="file"]')
    file_upload.clear()
    file_upload.send_keys(str(pathlib.Path(__file__).parent.parent / 'test.po'))
    selenium.find_element_by_css_selector('input[type="submit"]')
    assert 'File uploaded' in selenium.find_element_by_tag_name('body')
