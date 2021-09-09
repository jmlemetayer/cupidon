import logging
import os

from .auth import SynologyAuth
from .download import SynologyDownload
from .file import SynologyFile

from urllib.parse import urljoin

logger = logging.getLogger("synology")

class Synology():

    def __init__(self, environment, settings):
        self.environment = environment
        self.settings = settings

        self.auth = SynologyAuth(self)
        self.download = SynologyDownload(self)
        self.file = SynologyFile(self)

    def download_file(self, src_file, src_url, dst_file):
        dst_dir = os.path.dirname(dst_file)

        self.file.mkdir(dst_dir)

        self.download.download(src_url,
                destination=dst_dir,
                username=self.settings.get("seedbox.username"),
                password=self.settings.get("seedbox.password"))

    def download_movie(self, movie):
        src_file = movie["file"]

        src_urlpath = os.path.relpath(src_file, self.environment.root_dir)
        src_url = urljoin(self.settings.get("seedbox.url"), src_urlpath)

        dst_relfile = os.path.relpath(src_file, self.environment.movies_dir)
        dst_path = self.settings.get("synology.destination.movies")
        dst_file = os.path.join(dst_path, dst_relfile)

        self.download_file(src_file, src_url, dst_file)
