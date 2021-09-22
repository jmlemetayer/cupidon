import logging

import filesystem
from environment import Environment
from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask_socketio import SocketIO
from radarr import Radarr
from settings.toml import Settings
from synology import Synology

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("cupidon")

environment = Environment()

app = Flask(
    import_name=__name__,
    static_url_path="",
    static_folder=environment.www_dir,
    template_folder=environment.www_dir,
)

socketio = SocketIO(
    app=app,
    cors_allowed_origins=environment.cupidon_url or list(),
)

settings = Settings(
    environment=environment,
    socketio=socketio,
)

radarr = Radarr(
    environment=environment,
    settings=settings,
)

synology = Synology(
    environment=environment,
    settings=settings,
)


@app.errorhandler(404)
def not_found_error(error):
    return render_template("index.html")


@app.route("/radarr", methods=["POST"])
def radarr_webhook():
    app.logger.info(request.json)
    return Response(status=200)


@app.route("/sonarr", methods=["POST"])
def sonarr_webhook():
    app.logger.info(request.json)
    return Response(status=200)


@socketio.on("settings:read")
def read_settings():
    return settings.read()


@socketio.on("settings:update")
def update_settings(data):
    settings.update(data)


@socketio.on("movies:read")
def read_movies():
    return radarr.get_movies()


@socketio.on("movie:download")
def download_movie(movie):
    synology.download_movie(movie)


def dir_moved(dir_path, old_path):
    logger.info(f"directory moved from {old_path} to {dir_path}")


def dir_gone(dir_path):
    logger.info(f"directory gone {dir_path}")


def file_created(file_path):
    media_type = filesystem.get_file_media_type(file_path)
    file_inode = filesystem.get_file_inode(file_path)
    file_size = filesystem.get_file_size(file_path)
    logger.info(f"file created {file_path} {media_type} {file_inode} {file_size}")


def file_deleted(file_path):
    logger.info(f"file deleted {file_path}")


def file_gone(file_path):
    logger.info(f"file gone {file_path}")


def file_modified(file_path):
    logger.info(f"file modified {file_path}")


def file_moved(file_path, old_path):
    logger.info(f"file moved from {old_path} to {file_path}")


if __name__ == "__main__":
    filesystem.file_watcher(
        environment.data_dir,
        dir_moved=dir_moved,
        dir_gone=dir_gone,
        file_created=file_created,
        file_deleted=file_deleted,
        file_gone=file_gone,
        file_modified=file_modified,
        file_moved=file_moved,
    )

    socketio.run(app, host="0.0.0.0", port=8080)
