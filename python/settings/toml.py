import logging
import toml

from . import SettingsAbstract

logger = logging.getLogger("settings.toml")

class Settings(SettingsAbstract):

    def __init__(self, filename, environment):
        self.filename = filename
        self.data = None
        super().__init__(environment)

    def load(self, reload=None):
        if reload is None and self.data is not None:
            return self.data

        try:
            self.data = toml.load(self.filename)
        except FileNotFoundError:
            return dict()

        return self.data

    def dump(self, data):
        with open(self.filename, "w+") as f:
            toml.dump(data, f)

        self.data = data
