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
        settings["radarr"]["api_key"] = data.get("radarr", dict()).get("api_key", "")
        settings["sonarr"] = dict()
        settings["sonarr"]["api_key"] = data.get("sonarr", dict()).get("api_key", "")
        return settings

    def read(self):
        return self.format(self.load())

    def update(self, data):
        self.dump(self.format(data))
