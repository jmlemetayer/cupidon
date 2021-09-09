import hashlib
import logging
import os

from filesystem.media import *
from filesystem.watcher import *

logger = logging.getLogger("filesystem")

def get_file_inode(file_path):
    return os.stat(file_path).st_ino

def get_file_size(file_path):
    return os.stat(file_path).st_size

def get_file_md5sum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
