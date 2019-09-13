import os
import yaml


def yaml_import(config_dir):
    """ Extracts the configuration from a file """
    with open(os.path.join(config_dir, 'ci-config.yml'), 'r') as file:
        return yaml.safe_load(file)
