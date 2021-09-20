import logging
import os

logger = logging.getLogger("environment")


class Environment:
    def __init__(self):
        self.config_dir = os.environ.get("CONFIG_DIR", "/config")
        self.cupidon_url = os.environ.get("CUPIDON_URL", None)
        self.data_dir = os.environ.get("DATA_DIR", "/data")
        self.data_files_dir = os.environ.get(
            "DATA_FILES_DIR", os.path.join(self.data_dir, "files")
        )
        self.data_movies_dir = os.environ.get(
            "DATA_MOVIES_DIR", os.path.join(self.data_dir, "movies")
        )
        self.data_tv_shows_dir = os.environ.get(
            "DATA_TV_SHOWS_DIR", os.path.join(self.data_dir, "tv_shows")
        )
        self.radarr_data_dir = os.environ.get("RADARR_DATA_DIR", "/data")
        self.radarr_url = os.environ.get("RADARR_URL", "https://radarr.url")
        self.seedbox_url = os.environ.get("SEEDBOX_URL", "https://seedbox.url")
        self.sonarr_data_dir = os.environ.get("SONARR_DATA_DIR", "/data")
        self.sonarr_url = os.environ.get("SONARR_URL", "https://sonarr.url")
        self.www_dir = os.environ.get("WWW_DIR", "/www")

        logger.debug(f"config_dir:         {self.config_dir}")
        logger.debug(f"cupidon_url:        {self.cupidon_url}")
        logger.debug(f"data_dir:           {self.data_dir}")
        logger.debug(f"data_files_dir:     {self.data_files_dir}")
        logger.debug(f"data_movies_dir:    {self.data_movies_dir}")
        logger.debug(f"data_tv_shows_dir:  {self.data_tv_shows_dir}")
        logger.debug(f"radarr_data_dir:    {self.radarr_data_dir}")
        logger.debug(f"radarr_url:         {self.radarr_url}")
        logger.debug(f"seedbox_url:        {self.seedbox_url}")
        logger.debug(f"sonarr_data_dir:    {self.sonarr_data_dir}")
        logger.debug(f"sonarr_url:         {self.sonarr_url}")
        logger.debug(f"www_dir:            {self.www_dir}")
