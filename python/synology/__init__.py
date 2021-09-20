import logging
import os
import time
from urllib.parse import urljoin

import filesystem

from .auth import SynologyAuth
from .download import SynologyDownload
from .file import SynologyFile

logger = logging.getLogger("synology")


class Synology:
    def __init__(self, environment, settings):
        self.environment = environment
        self.settings = settings

        self.auth = SynologyAuth(self)
        self.download = SynologyDownload(self)
        self.file = SynologyFile(self)

    def file_exist(self, src_file, dst_file):
        dst_filename = os.path.basename(dst_file)
        dst_dir = os.path.dirname(dst_file)

        rmt_files = self.file.list(dst_dir)["files"]
        rmt_file = next((f for f in rmt_files if f["name"] == dst_filename), None)

        if rmt_file is None:
            return False

        logger.debug(f"The remote file {dst_filename} already exists")

        src_file_size = filesystem.get_file_size(src_file)

        if rmt_file["additional"]["size"] != src_file_size:
            return False

        logger.debug(f"The remote file {dst_filename} has the same size")

        rmt_file_md5_taskid = self.file.md5_start(dst_file)["taskid"]
        src_file_md5 = filesystem.get_file_md5sum(src_file)
        rmt_file_md5_status = self.file.md5_status(rmt_file_md5_taskid)

        while rmt_file_md5_status["finished"] is not True:
            time.sleep(10)
            rmt_file_md5_status = self.file.md5_status(rmt_file_md5_taskid)

        rmt_file_md5 = rmt_file_md5_status["md5"]

        if src_file_md5 != rmt_file_md5:
            return False

        logger.debug(f"The remote file {dst_filename} is identical")

        return True

    def download_file(self, src_file, src_url, dst_file):
        dst_filename = os.path.basename(dst_file)
        dst_dir = os.path.dirname(dst_file)

        self.file.mkdir(dst_dir)

        if self.file_exist(src_file, dst_file):
            logger.info(f"The downloading of the file {dst_filename} has been skipped")
            return

        self.download.download(
            src_url,
            destination=dst_dir,
            username=self.settings.get("seedbox.username"),
            password=self.settings.get("seedbox.password"),
        )

    def download_movie(self, movie):
        src_file = movie["file"]

        src_urlpath = os.path.relpath(src_file, self.environment.data_dir)
        src_url = urljoin(self.settings.get("seedbox.url"), src_urlpath)

        dst_relfile = os.path.relpath(src_file, self.environment.movies_dir)
        dst_path = self.settings.get("synology.destination.movies")
        dst_file = os.path.join(dst_path, dst_relfile)

        self.download_file(src_file, src_url, dst_file)
