import os
import yaml


def yaml_import(root_dir):
    """ Extracts the configuration from a file """
    with open(os.path.join(root_dir, 'ci-config.yml'), 'r') as file:
        return yaml.safe_load(file)
