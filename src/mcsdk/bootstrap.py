import os
from .integration import validator
from .integration import configurator

# Check if the environment if properly set up
validator.validate_env()

# Define constants
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
TRAVIS_BUILD_DIR = os.environ.get('TRAVIS_BUILD_DIR')
TRAVIS_ROOT_DIR = os.path.dirname(TRAVIS_BUILD_DIR)
TRAVIS_BASE_BRANCH = os.environ.get('BASE_BRANCH')
TRAVIS_HEAD_BRANCH = os.environ.get('HEAD_BRANCH')

# Define global vars
resources_dir = os.path.join(TRAVIS_BUILD_DIR, 'resources')
config_dir = os.path.join(resources_dir, 'config')
templates_dir = os.path.join(resources_dir, 'templates')

# Loading the configuration
cfg = configurator.yaml_import(config_dir)
cfg['repos']['core']['dir'] = os.path.abspath(os.path.join(TRAVIS_ROOT_DIR, cfg['repos']['core']['name']))
cfg['repos']['sdk']['dir'] = os.path.abspath(os.path.join(TRAVIS_ROOT_DIR, cfg['repos']['sdk']['name']))

# Custom stuff...manual work for now
rep = ['{%repos_core_dir%}', cfg['repos']['core']['dir']]

# Fix paths
cfg['repos']['core']['swagger_cli'] = os.sep.join(str(cfg['repos']['core']['swagger_cli']).split("/"))
cfg['repos']['core']['swagger_spec'] = os.sep.join(str(cfg['repos']['core']['swagger_spec']).split("/"))

# Replace placeholder
cfg['repos']['core']['swagger_cli'] = str(cfg['repos']['core']['swagger_cli']).replace(rep[0], rep[1])
cfg['repos']['core']['swagger_spec'] = str(cfg['repos']['core']['swagger_spec']).replace(rep[0], rep[1])
