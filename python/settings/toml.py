import logging
import toml

from . import SettingsAbstract

logger = logging.getLogger("settings.toml")

class SettingsToml(SettingsAbstract):

    def __init__(self, filename):
        self.filename = filename
        super().__init__()

    def load(self):
        try:
            return toml.load(self.filename)
        except FileNotFoundError:
            return dict()

    def dump(self, data):
        with open(self.filename, "w+") as f:
            toml.dump(data, f)
