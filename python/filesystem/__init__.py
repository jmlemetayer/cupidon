import logging
import os

from filesystem.media import *
from filesystem.watcher import *

logger = logging.getLogger("filesystem")

def get_file_inode(file_path):
    return os.stat(file_path).st_ino

def get_file_size(file_path):
    return os.stat(file_path).st_size
