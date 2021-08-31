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
        settings["radaar"] = dict()
        settings["radaar"]["api_key"] = data.get("radaar", dict()).get("api_key", "")
        settings["sonaar"] = dict()
        settings["sonaar"]["api_key"] = data.get("sonaar", dict()).get("api_key", "")
        return settings

    def read(self):
        return self.format(self.load())

    def update(self, data):
        self.dump(self.format(data))
