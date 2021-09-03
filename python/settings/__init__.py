import logging

from abc import ABC, abstractmethod

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
        settings["radarr"]["url"] = data.get("radarr", dict()).get("url", "http://localhost")
        settings["radarr"]["api_key"] = data.get("radarr", dict()).get("api_key", "")
        settings["sonarr"] = dict()
        settings["sonarr"]["url"] = data.get("sonarr", dict()).get("url", "http://localhost")
        settings["sonarr"]["api_key"] = data.get("sonarr", dict()).get("api_key", "")
        return settings

    def read(self, **kwargs):
        return self.format(self.load(**kwargs))

    def update(self, data, **kwargs):
        self.dump(self.format(data), **kwargs)
