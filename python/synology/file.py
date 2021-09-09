import logging
import os

logger = logging.getLogger("synology.file")

class SynologyFile():

    def __init__(self, parent):
        self.parent = parent

    def folder_path(self, path):
        return os.path.join("/", path.lstrip("/"))

    def mkdir(self, *paths):
        folder_paths = list()
        names = list()

        for path in paths:
            folder_paths.append(self.folder_path(os.path.dirname(path)))
            names.append(os.path.basename(path))

        data = dict()
        data["force_parent"] = True
        data["folder_path"] = folder_paths
        data["name"] = names

        self.parent.auth.request("SYNO.FileStation.CreateFolder", "create", data)
