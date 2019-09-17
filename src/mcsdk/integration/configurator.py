import yaml


def yaml_import(config_file):
    """ Extracts the configuration from a file """
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)
