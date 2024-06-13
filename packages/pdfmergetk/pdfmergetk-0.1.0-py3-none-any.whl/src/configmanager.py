# -*- coding: utf-8 -*-
"""
ConfigManager : in charge to manages configuration of app.
"""

import os
import sys

import json

from typing import Union


class ConfigManager:
    """
    In charge to load, save configuration of app.
    """
    app = 'pdfmergetk'
    file = 'appconfig.json'

    def __init__(self) -> None:
        """
        Constructor
        """
        self.path_config = None
        self.path_config_file = None
        self.current_platform = None
        self.start()

    def start(self) -> None:
        """
        Main method in charge of obtaining platform, sets directory path and
        app configuration file.
        """
        self.current_platform = sys.platform.lower()

        if self.current_platform == 'darwin':
            path_config = os.path.join(
                            os.path.expanduser('~'),
                            "Library",
                            "Application Support",
                            ConfigManager.app
                        )
        elif self.current_platform == 'linux':
            path_config = os.path.join(
                            os.path.expanduser('~'),
                            ".config",
                            ConfigManager.app
                        )
        elif self.current_platform == 'win32':
            path_config = os.path.join(
                            os.getenv('LOCALAPPDATA'),
                            ConfigManager.app
                        )
        else:
            # Platform Error.
            path_config = None

        self.path_config = path_config
        self.path_config_file = os.path.join(
                                    self.path_config,
                                    ConfigManager.file
                                )

        if not os.path.exists(self.path_config):
            os.makedirs(self.path_config)

    def save_config(
        self,
        config: dict
    ) -> None:
        """
        Saves configuration of app.
        """
        with open(self.path_config_file, 'w') as file:
            file.write(json.dumps(config))

    def load_config(self) -> Union[dict, None]:
        """
        Loads configuration of app.
        """
        try:
            with open(self.path_config_file, 'r') as file:
                return json.loads(file.readline())
        except FileNotFoundError:
            return None

    def __str__(self) -> str:
        """
        Returns a representation of instance.
        """
        return '<[ Config: %s, Plat: %s ]>' % (
                            self.path_config_file,
                            self.current_platform
                        )
