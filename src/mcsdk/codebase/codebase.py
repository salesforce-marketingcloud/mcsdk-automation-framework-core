import os
from abc import ABC, abstractmethod


class AbstractCodebase(ABC):
    def __init__(self, root_dir, config, folder):
        """ Codebase class constructor """
        self._root_dir = root_dir
        self._config = config
        self._repo_folder = folder
        self._package_folder = os.path.join(self._repo_folder, self._config['repos']['sdk']['packageName'])


class AbstractCodeSetup(AbstractCodebase):
    """ Handles the code setup processes """

    @abstractmethod
    def install_dependencies(self):
        ...


class AbstractCodeIntegration(AbstractCodebase):
    """ Handles the code integration processes """

    @abstractmethod
    def run_tests(self):
        ...
