# IMPORTS
import json
import os
from typing import Any, Dict

from retdec_config_patch.paths import get_retdec_share_folder

# CONSTANTS
CONFIG_FILE = os.path.abspath(os.path.join(get_retdec_share_folder(), "patch-config.json"))


# CLASSES
class Config:
    """
    Class containing configuration options.
    """

    fields = ["retdec_binary"]

    def __init__(self):
        """
        Initializes a blank configuration option object.
        """

        self.retdec_binary: str = None

    # Magic methods
    def __repr__(self) -> str:
        return "<RetDec Configuration>"

    def __str__(self) -> str:
        return str(self._serialize())

    # Helper methods
    def _serialize(self) -> Dict[str, Any]:
        """
        Serializes the contents of the configuration file.

        :return: dictionary representing the configuration options
        """

        return {field: getattr(self, field) for field in self.fields}

    def _deserialize(self, config_dict: Dict[str, Any]):
        """
        Sets the configuration options based on the provided dictionary.

        :param config_dict: configuration dictionary
        """

        for key, value in config_dict.items():
            setattr(self, key, value)

    # Public methods
    @classmethod
    def load(cls, filepath: os.PathLike = CONFIG_FILE) -> "Config":
        """
        Loads configuration from a JSON file.

        If no file is found, loads empty config.

        :param filepath: path to the configuration file
        :return: loaded configuration object
        """

        config = cls()

        try:
            with open(filepath, "r") as f:
                config_dict = json.load(f)
                config._deserialize(config_dict)
        except FileNotFoundError:
            pass

        return config

    def save(self, filepath: os.PathLike = CONFIG_FILE):
        """
        Saves configuration to a JSON file.

        :param filepath: path to the configuration file
        """

        config_dict = self._serialize()
        with open(filepath, "w") as f:
            json.dump(config_dict, f)

    @staticmethod
    def remove(filepath: os.PathLike = CONFIG_FILE):
        """
        Removes the configuration file.

        :param filepath: path to the configuration file
        """

        os.remove(filepath)

    def is_empty(self):
        values = list(self._serialize().values())
        is_none = [value is None for value in values]
        return all(is_none)
