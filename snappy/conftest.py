import os

ROOT_CONFIG_REPO = "/home/legionarius/Code/snappy_repos/configs"

def pytest_addoption(parser):
    group = parser.getgroup('test-config')

    group.addoption(
        '--config',
        action='store',
        dest='config_file',
        help='The configuration file to use for this test run.'
    )

def pytest_configure(config):
    if config.getoption('config_file'):
        _set_config_file(config.getoption('config_file'))


def _set_config_file(config_path):
    os.environ['TEST_CONFIG'] = os.path.abspath(config_path)