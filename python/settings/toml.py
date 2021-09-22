import logging
import os

import toml

from . import SettingsAbstract

logger = logging.getLogger("settings.toml")


class Settings(SettingsAbstract):
    def __init__(self, environment, socketio):
        self.config_file = os.path.join(environment.config_dir, "cupidon.conf")
        self.data = None
        super().__init__(environment, socketio)
        self.file_watcher(self.config_file)

    def load(self, reload=None):
        if reload is None and self.data is not None:
            return self.data

        try:
            self.data = toml.load(self.config_file)
        except FileNotFoundError:
            return dict()

        return self.data

    def dump(self, data):
        with open(self.config_file, "w+") as f:
            toml.dump(data, f)

        self.data = data
