import logging
import requests

from urllib.parse import urljoin

logger = logging.getLogger("radarr")

class Radarr():

    def __init__(self, settings):
        self.settings = settings

    def request(self, method, path, params=None, json=None):
        base_url = self.settings.get("radarr.url")
        api_url = urljoin(base_url, "api/v3/")
        url = urljoin(api_url, path)

        if params is None:
            params = dict()
        params["apiKey"] = self.settings.get("radarr.api_key")

        response = requests.request(method, url, params=params, json=json)
        assert response.ok
        return response.json()

    def format_movie(self, movie):
        formatted_movie = dict()
        formatted_movie["id"] = movie["id"]
        formatted_movie["title"] = movie.get("originalTitle") or movie["title"]
        formatted_movie["path"] = movie.get("path")
        formatted_movie["file"] = movie.get("movieFile", dict()).get("path")
        return formatted_movie

    def get_movies(self):
        movies = self.request("GET", "movie")
        formatted_movies = [self.format_movie(m) for m in movies]
        return sorted(formatted_movies, key=lambda k: k["id"], reverse=True)

    def get_movie(self, id):
        return self.format_movie(self.request("GET", f"movie/{id}"))
