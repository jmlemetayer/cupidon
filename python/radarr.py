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

    def format_movie(self, movie, queue=None):
        formatted_movie = {
            "id": movie["id"],
            "title": movie.get("originalTitle") or movie["title"],
            "path": movie.get("path"),
            "file": movie.get("movieFile", dict()).get("path"),
            "tags": [],
        }

        if movie.get("hasFile", False) is False:
            formatted_movie["tags"].append("unavailable")

        movie_queue = self.get_movie_queue(movie["id"], queue=queue)
        if movie_queue is not None:
            formatted_movie["tags"].append(movie_queue["status"])

        return formatted_movie

    def get_movies(self):
        movies = self.request("GET", "movie")
        queue = self.get_queue()
        formatted_movies = [self.format_movie(m, queue=queue) for m in movies]
        return sorted(formatted_movies, key=lambda k: k["id"], reverse=True)

    def get_movie(self, id):
        return self.format_movie(self.request("GET", f"movie/{id}"))

    def get_queue(self):
        return self.request("GET", "queue")

    def get_movie_queue(self, id, queue=None):
        if queue is None:
            queue = self.get_queue()
        return next((x for x in queue["records"] if x["movieId"] == id), None)
