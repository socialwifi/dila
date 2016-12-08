import os
from dila import config


def initialize_config():
    if 'DILA_CONFIG_MODULE' in os.environ:
        module_name = os.environ['DILA_CONFIG_MODULE']
        config.setup_from_module(module_name)
