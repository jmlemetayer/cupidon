import logging
import os

logger = logging.getLogger("environment")

class Environment():

    def __init__(self):
        self.cupidon_url       = os.environ.get("CUPIDON_URL", None)
        self.seedbox_url       = os.environ.get("SEEDBOX_URL", "https://seedbox.url")
        self.config_dir        = os.environ.get("CONFIG_DIR", "/config")
        self.data_dir          = os.environ.get("DATA_DIR", "/data")
        self.data_files_dir    = os.environ.get("DATA_FILES_DIR", os.path.join(self.data_dir, "files"))
        self.data_movies_dir   = os.environ.get("DATA_MOVIES_DIR", os.path.join(self.data_dir, "movies"))
        self.data_tv_shows_dir = os.environ.get("DATA_TV_SHOWS_DIR", os.path.join(self.data_dir, "tv_shows"))
        self.www_dir           = os.environ.get("WWW_DIR", "/www")

        logger.debug(f"cupidon_url:        {self.cupidon_url}")
        logger.debug(f"seedbox_url:        {self.seedbox_url}")
        logger.debug(f"config_dir:         {self.config_dir}")
        logger.debug(f"data_dir:           {self.data_dir}")
        logger.debug(f"data_files_dir:     {self.data_files_dir}")
        logger.debug(f"data_movies_dir:    {self.data_movies_dir}")
        logger.debug(f"data_tv_shows_dir:  {self.data_tv_shows_dir}")
        logger.debug(f"www_dir:            {self.www_dir}")
