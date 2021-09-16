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
        return {
            "radarr": {
                "url": self.get("radarr.url", self.environment.radarr_url, data),
                "api_key": self.get("radarr.api_key", "", data),
            },
            "sonarr": {
                "url": self.get("sonarr.url", self.environment.sonarr_url, data),
                "api_key": self.get("sonarr.api_key", "", data),
            },
            "seedbox": {
                "url": self.get("seedbox.url", self.environment.seedbox_url, data),
                "username": self.get("seedbox.username", "", data),
                "password": self.get("seedbox.password", "", data),
            },
            "synology": {
                "url": self.get("synology.url", "https://synology.url", data),
                "username": self.get("synology.username", "", data),
                "password": self.get("synology.password", "", data),
                "destination": {
                    "movies": self.get("synology.destination.movies", "", data),
                    "tv_shows": self.get("synology.destination.tv_shows", "", data),
                    "others": self.get("synology.destination.others", "", data),
                },
            },
        }

    def read(self, **kwargs):
        return self.format(self.load(**kwargs))

    def update(self, data, **kwargs):
        self.dump(self.format(data), **kwargs)

    def get(self, path, default=None, data=None):
        if data is None:
            data = self.read()
        return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, path.split("."), data)
