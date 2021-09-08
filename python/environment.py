import logging
import os

logger = logging.getLogger("environment")

class Environment():

    def __init__(self):
        self.cupidon_url    = os.environ.get("CUPIDON_URL", None)
        self.seedbox_url    = os.environ.get("SEEDBOX_URL", "https://seedbox.url")
        self.config_dir     = os.environ.get("CONFIG_DIR", "/config")
        self.root_dir       = os.environ.get("ROOT_DIR", "/downloads")
        self.downloaded_dir = os.environ.get("DOWNLOADED_DIR", "/downloads/Downloaded")
        self.movies_dir     = os.environ.get("MOVIES_DIR", "/downloads/Movies")
        self.tv_shows_dir   = os.environ.get("TV_SHOWS_DIR", "/downloads/TV Shows")

        logger.debug(f"cupidon_url:     {self.cupidon_url}")
        logger.debug(f"seedbox_url:     {self.seedbox_url}")
        logger.debug(f"config_dir:      {self.config_dir}")
        logger.debug(f"root_dir:        {self.root_dir}")
        logger.debug(f"downloaded_dir:  {self.downloaded_dir}")
        logger.debug(f"movies_dir:      {self.movies_dir}")
        logger.debug(f"tv_shows_dir:    {self.tv_shows_dir}")
