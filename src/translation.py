from flask import Flask, send_from_directory, render_template, jsonify, redirect, url_for
import os
from record_and_stream import StreamRecorder


app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE_FOLDER = os.path.join(BASE_DIR, "archive")
LIVE_FOLDER = os.path.join(BASE_DIR, "live")

recorder = StreamRecorder(
    rtsp_url="rtsp://192.168.1.75:8080/h264_pcm.sdp",
    archive_folder=ARCHIVE_FOLDER,
    live_folder=LIVE_FOLDER,
)
recorder.start_recording()

@app.route("/")
def index():
    all_files = sorted(
        [f for f in os.listdir(ARCHIVE_FOLDER) if f.endswith(".mp4")],
        reverse=True
    )
    
    files = all_files[1:]

    return render_template("index.html", files=files)

@app.route("/archive/<path:filename>")
def archive_file(filename):
    return send_from_directory(ARCHIVE_FOLDER, filename)

@app.route("/live/<path:filename>")
def live_file(filename):
    return send_from_directory(LIVE_FOLDER, filename)

@app.route("/restart_recording", methods=["POST"])
def restart_recording():
    recorder.restart_recording()
    return redirect(url_for('index'))  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)