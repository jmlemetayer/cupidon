import filesystem
import logging
import os

from settings.toml import SettingsToml

from flask import Flask, Response, render_template, request
from flask_socketio import SocketIO, emit

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("cupidon")

config_dir = os.environ.get("CONFIG_DIR", "/config")
downloaded_dir = os.environ.get("DOWNLOADED_DIR", "/downloads/Downloaded")
movies_dir = os.environ.get("MOVIES_DIR", "/downloads/Movies")
tv_shows_dir = os.environ.get("TV_SHOWS_DIR", "/downloads/TV Shows")

settings = SettingsToml(os.path.join(config_dir, "cupidon.conf"))

app = Flask(__name__,
            static_url_path="",
            static_folder="/www",
            template_folder="/www")

socketio = SocketIO(app)

@app.errorhandler(404)
def not_found_error(error):
    return render_template("index.html")

@app.route("/radarr", methods=["POST"])
def radarr():
    app.logger.info(request.json)
    return Response(status=200)

@app.route("/sonarr", methods=["POST"])
def sonarr():
    app.logger.info(request.json)
    return Response(status=200)

@socketio.event
def my_event(message):
    emit("my response", {"data": "got it!"})

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

    socketio.run(app, host="0.0.0.0", port=8080)
