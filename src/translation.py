from flask import Flask, send_from_directory, render_template
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARCHIVE_FOLDER = os.path.join(BASE_DIR, "archive")
LIVE_FOLDER = os.path.join(BASE_DIR, "live")

@app.route("/")
def index():
    files = sorted(
        [f for f in os.listdir(ARCHIVE_FOLDER) if f.endswith(".mp4")],
        reverse=True
    )
    return render_template("index.html", files=files)

@app.route("/archive/<path:filename>")
def archive_file(filename):
    return send_from_directory(ARCHIVE_FOLDER, filename)

@app.route("/live/<path:filename>")
def live_file(filename):
    return send_from_directory(LIVE_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
