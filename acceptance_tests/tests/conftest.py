import pathlib

import pytest
import sh
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@pytest.fixture(scope="session")
def docker_image():
    build_script = pathlib.Path(__file__).parent.parent / 'test_image' / 'build.sh'
    build = sh.Command(str(build_script))
    image_name = 'test_dila_image'
    build(image_name)
    yield image_name


@pytest.fixture(scope="session")
def running_server(docker_image):
    container_name = 'test_dila'
    sh.docker('run', '-d', '--name', container_name, docker_image)
    yield container_name
    sh.docker('rm', '-fv', container_name)


@pytest.fixture(scope="session")
def running_server_ip(running_server):
    return get_container_ip(running_server)


@pytest.fixture(scope="session")
def running_server_url(running_server_ip):
    return 'http://' + running_server_ip


@pytest.fixture(scope="session")
def selenium_server():
    container_name = 'test_dila_selenium'
    sh.docker('run', '-d', '--name', container_name, 'selenium/standalone-firefox')
    log = sh.docker('logs', '-f', container_name, _iter=True)
    for line in log:
        if 'Selenium Server is up and running' in line:
            break
    log.terminate()
    yield container_name
    sh.docker('rm', '-fv', container_name)


@pytest.fixture(scope="session")
def selenium_server_ip(selenium_server):
    return get_container_ip(selenium_server)


@pytest.fixture(scope="session")
def selenium(selenium_server_ip):
    remote = webdriver.Remote('http://{}:4444/wd/hub'.format(selenium_server_ip), desired_capabilities=DesiredCapabilities.FIREFOX)
    yield remote
    remote.quit()


def get_container_ip(container_name):
    return sh.docker(
        'inspect', '-f', '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', container_name).strip()
