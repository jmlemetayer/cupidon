import logging
import os
from abc import ABC
from abc import abstractmethod
from functools import reduce

import filesystem

logger = logging.getLogger("settings")


class SettingsAbstract(ABC):
    def __init__(self, environment, socketio):
        self.environment = environment
        self.socketio = socketio
        self.load()

    @abstractmethod
    def load(self, reload=None, **kwargs):
        pass

    @abstractmethod
    def dump(self, data, **kwargs):
        pass

    def file_watcher(self, config_file):
        def file_updated(file_path):
            if file_path == config_file:
                self.socketio.emit("settings:updated", self.read(reload=True))

        filesystem.file_watcher(
            os.path.dirname(config_file),
            file_created=file_updated,
            file_modified=file_updated,
        )

    def format(self, data):
        return {
            "radarr": {
                "url": self.get("radarr.url", self.environment.radarr_url, data),
                "api_key": self.get("radarr.api_key", "", data),
                "data_dir": self.get(
                    "radarr.data_dir", self.environment.radarr_data_dir, data
                ),
            },
            "sonarr": {
                "url": self.get("sonarr.url", self.environment.sonarr_url, data),
                "api_key": self.get("sonarr.api_key", "", data),
                "data_dir": self.get(
                    "sonarr.data_dir", self.environment.sonarr_data_dir, data
                ),
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
                    "files": self.get("synology.destination.files", "", data),
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
        return reduce(
            lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
            path.split("."),
            data,
        )
