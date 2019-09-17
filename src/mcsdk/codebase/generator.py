from abc import ABC, abstractmethod


class AbstractGenerator(ABC):
    """ Handles the Swagger codegen process but also custom generation processes """

    def __init__(self, root_dir, config, config_dir, templates_dir, repo_dir):
        """ Class constructor """
        self._root_dir = root_dir
        self._config = config
        self._config_dir = config_dir
        self._templates_dir = templates_dir
        self._repo_dir = repo_dir

    @abstractmethod
    def generate(self):
        """ Generates the SDK code """
        ...
