import pathlib
import uuid

import pytest
import sh
import time
from selenium import webdriver
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

RESOURCES_PATH = pathlib.Path(__file__).parent.parent.parent / 'test_resources'


@pytest.fixture(scope="session")
def docker_image():
    build_script = RESOURCES_PATH / 'test_image' / 'build.sh'
    build = sh.Command(str(build_script))
    image_name = 'test_dila_image'
    build(image_name)
    yield image_name

@pytest.fixture(scope="session")
def unmigrated_postgres_server():
    container_name = 'acceptance_test_dila_postgres'
    sh.docker('run', '-d', '-e', 'POSTGRES_USER=dila', '-e', 'POSTGRES_PASSWORD=dila', '--name', container_name,
              'postgres')
    log = sh.docker('logs', '-f', container_name, _iter=True, _ok_code=2)
    for line in log:
        if 'PostgreSQL init process complete; ready for start up.' in line:
            break
    log.terminate()
    yield container_name
    sh.docker('rm', '-fv', container_name)


@pytest.fixture
def postgres_server(unmigrated_postgres_server, docker_image):
    sh.docker('run', '--rm', '--link', '{}:db'.format(unmigrated_postgres_server), docker_image,
              'alembic', '-c', 'dila/alembic.ini', 'upgrade', 'head')
    yield unmigrated_postgres_server
    sh.docker('run', '--rm', '--net', 'container:{}'.format(unmigrated_postgres_server),
              '-e', 'POSTGRES_USER=dila', '-e', 'POSTGRES_PASSWORD=dila', 'postgres',
              'psql', '-h', 'localhost', '-U', 'dila', '-c', 'DROP SCHEMA public CASCADE; CREATE SCHEMA public;')


@pytest.fixture(scope="session")
def ldap_server():
    container_name = 'acceptance_test_dila_ldap'
    script_path = str(RESOURCES_PATH / 'test.ldif')
    sh.docker('run', '-d', '-e', 'LDAP_ORGANISATION="Dila"', '-e', 'LDAP_DOMAIN=example.com',
              '-e', 'LDAP_ADMIN_PASSWORD=admin_password',
              '-v', '{}:/scripts/test.ldif:ro'.format(script_path),
              '--name', container_name, 'osixia/openldap')
    log = sh.docker('logs', '-f', container_name, _iter='err', _ok_code=2)
    for line in log:
        if 'slapd starting' in line:
            break
    log.terminate()
    sh.docker('exec', container_name,
              'ldapadd', '-x', '-D', 'cn=admin,dc=example,dc=com', '-w', 'admin_password', '-f', '/scripts/test.ldif')
    yield container_name
    sh.docker('rm', '-fv', container_name)


@pytest.fixture
def running_server(postgres_server, ldap_server, docker_image):
    container_name = 'test_dila'
    sh.docker('run', '-d', '--name', container_name, '--link', '{}:db'.format(postgres_server),
              '--link', '{}:ldap'.format(ldap_server), docker_image)
    log = sh.docker('logs', '-f', container_name, _iter='err', _ok_code=2)
    for line in log:
        if 'Running on http://0.0.0.0:80/' in line:
            break
    log.terminate()
    yield container_name
    sh.docker('rm', '-fv', container_name)


@pytest.fixture
def running_server_ip(running_server):
    return get_container_ip(running_server)


@pytest.fixture
def running_server_url(running_server_ip):
    return 'http://' + running_server_ip + '/'


@pytest.fixture(scope="session")
def selenium_server():
    container_name = 'test_dila_selenium'
    sh.docker('run', '-d', '--name', container_name, 'selenium/standalone-firefox')
    log = sh.docker('logs', '-f', container_name, _iter=True, _ok_code=2)
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
    remote.implicitly_wait(2)
    yield remote
    remote.quit()


def get_container_ip(container_name):
    return sh.docker(
        'inspect', '-f', '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', container_name).strip()

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    selenium = item.funcargs.get('selenium', None)
    if selenium and report.when == 'call':
        report.sections.append(('selenium', '\n'.join(get_selenium_summary(selenium))))


def get_selenium_summary(selenium: webdriver.Remote):
    try:
        yield 'current_url: {}'.format(selenium.current_url)
        screenshot = '/tmp/{}.png'.format(uuid.uuid4())
        with open(screenshot, 'wb') as f:
            f.write(selenium.get_screenshot_as_png())
        yield 'screenshot: {}'.format(screenshot)
    except selenium_exceptions.WebDriverException:
        yield 'FAILED TO GET SELENIUM DATA.'
