from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__,
            static_url_path="",
            static_folder="/www",
            template_folder="/www")

socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.event
def my_event(message):
    emit("my response", {"data": "got it!"})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)
