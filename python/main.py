import filesystem
import logging
import os

from radarr import Radarr
from settings.toml import SettingsToml

from flask import Flask, Response, render_template, request
from flask_socketio import SocketIO

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("cupidon")

config_dir = os.environ.get("CONFIG_DIR", "/config")
downloaded_dir = os.environ.get("DOWNLOADED_DIR", "/downloads/Downloaded")
movies_dir = os.environ.get("MOVIES_DIR", "/downloads/Movies")
tv_shows_dir = os.environ.get("TV_SHOWS_DIR", "/downloads/TV Shows")

config_file = os.path.join(config_dir, "cupidon.conf")
settings = SettingsToml(config_file)

radarr = Radarr(settings)

app = Flask(__name__,
            static_url_path="",
            static_folder="/www",
            template_folder="/www")

# Enable origin check only if an origin is provided
cors_allowed_origins = os.environ.get("CUPIDON_ORIGIN", list())

socketio = SocketIO(app, cors_allowed_origins=cors_allowed_origins)

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

def config_file_updated(file_path):
    if file_path == config_file:
        socketio.emit("settings:updated", settings.read(reload=True))

@socketio.on("movies:read")
def read_movies():
    return radarr.get_movies()

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
    logger.info(f"config_dir = {config_dir}")
    logger.info(f"downloaded_dir = {downloaded_dir}")
    logger.info(f"movies_dir = {movies_dir}")
    logger.info(f"tv_shows_dir = {tv_shows_dir}")

    filesystem.file_watcher([downloaded_dir, movies_dir, tv_shows_dir],
                            dir_moved=dir_moved,
                            dir_gone=dir_gone,
                            file_created=file_created,
                            file_deleted=file_deleted,
                            file_gone=file_gone,
                            file_modified=file_modified,
                            file_moved=file_moved)

    filesystem.file_watcher([config_dir],
                            file_created=config_file_updated,
                            file_modified=config_file_updated)

    socketio.run(app, host="0.0.0.0", port=8080)
