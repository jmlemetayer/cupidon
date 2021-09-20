import logging
import os

logger = logging.getLogger("synology.file")


class SynologyFile:
    def __init__(self, parent):
        self.parent = parent

    def folder_path(self, path):
        return os.path.join("/", path.lstrip("/"))

    def list(self, path):
        data = dict()
        data["folder_path"] = self.folder_path(path)
        data["additional"] = ["size"]
        return self.parent.auth.request("SYNO.FileStation.List", "list", data)

    def md5_start(self, path):
        data = dict()
        data["file_path"] = self.folder_path(path)
        return self.parent.auth.request("SYNO.FileStation.MD5", "start", data)

    def md5_status(self, taskid):
        data = dict()
        data["taskid"] = taskid
        return self.parent.auth.request("SYNO.FileStation.MD5", "status", data)

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
