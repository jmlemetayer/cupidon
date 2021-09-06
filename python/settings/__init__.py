import logging

from abc import ABC, abstractmethod
from functools import reduce

logger = logging.getLogger("settings")

class SettingsAbstract(ABC):

    def __init__(self):
        self.load()

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def dump(self, data):
        pass

    def format(self, data):
        settings = dict()
        settings["radarr"] = dict()
        settings["radarr"]["url"]     = self.get("radarr.url", "http://localhost", data)
        settings["radarr"]["api_key"] = self.get("radarr.api_key", "", data)
        settings["sonarr"] = dict()
        settings["sonarr"]["url"]     = self.get("sonarr.url", "http://localhost", data)
        settings["sonarr"]["api_key"] = self.get("sonarr.api_key", "", data)
        return settings

    def read(self, **kwargs):
        return self.format(self.load(**kwargs))

    def update(self, data, **kwargs):
        self.dump(self.format(data), **kwargs)

    def get(self, path, default=None, data=None):
        if data is None:
            data = self.read()
        return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, path.split("."), data)
