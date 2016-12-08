import selenium.webdriver


def test_first(selenium: selenium.webdriver.Remote, running_server_url):
    selenium.get(running_server_url + '/strings')
    assert selenium.title == '404 Not Found'
