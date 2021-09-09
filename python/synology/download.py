import logging

from urllib.parse import quote

logger = logging.getLogger("synology.download")

class SynologyDownload():

    def __init__(self, parent):
        self.parent = parent

    def download(self, *urls, destination, username=None, password=None):
        data = dict()
        data["create_list"] = True
        data["type"] = "url"
        data["url"] = urls
        data["destination"] = destination.lstrip("/")

        if username is not None:
            data["username"] = username
        if password is not None:
            data["password"] = password

        self.parent.auth.request("SYNO.DownloadStation2.Task", "create", data)
