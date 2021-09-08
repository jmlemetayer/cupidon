import logging

from abc import ABC, abstractmethod
from functools import reduce

logger = logging.getLogger("settings")

class SettingsAbstract(ABC):

    def __init__(self, environment):
        self.environment = environment
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
        settings["radarr"]["url"]     = self.get("radarr.url", "https://radarr.url", data)
        settings["radarr"]["api_key"] = self.get("radarr.api_key", "", data)
        settings["sonarr"] = dict()
        settings["sonarr"]["url"]     = self.get("sonarr.url", "https://sonarr.url", data)
        settings["sonarr"]["api_key"] = self.get("sonarr.api_key", "", data)
        settings["seedbox"] = dict()
        settings["seedbox"]["url"]      = self.get("seedbox.url", self.environment.seedbox_url, data)
        settings["seedbox"]["username"] = self.get("seedbox.username", "", data)
        settings["seedbox"]["password"] = self.get("seedbox.password", "", data)
        settings["synology"] = dict()
        settings["synology"]["url"]      = self.get("synology.url", "https://synology.url", data)
        settings["synology"]["username"] = self.get("synology.username", "", data)
        settings["synology"]["password"] = self.get("synology.password", "", data)
        settings["synology"]["destination"] = dict()
        settings["synology"]["destination"]["movies"]   = self.get("synology.destination.movies", "", data)
        settings["synology"]["destination"]["tv_shows"] = self.get("synology.destination.tv_shows", "", data)
        settings["synology"]["destination"]["others"]   = self.get("synology.destination.others", "", data)
        return settings

    def read(self, **kwargs):
        return self.format(self.load(**kwargs))

    def update(self, data, **kwargs):
        self.dump(self.format(data), **kwargs)

    def get(self, path, default=None, data=None):
        if data is None:
            data = self.read()
        return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, path.split("."), data)
