import ffmpeg
import os

# Настройки
RTSP_URL = "rtsp://192.168.1.75:8080/h264_pcm.sdp"
ARCHIVE_FOLDER = "./archive"
LIVE_FOLDER = "./live"

os.makedirs(ARCHIVE_FOLDER, exist_ok=True)
os.makedirs(LIVE_FOLDER, exist_ok=True)

input_stream = ffmpeg.input(RTSP_URL, rtsp_transport='tcp', fflags='+genpts')

archive_output = ffmpeg.output(
    input_stream,
    f'{ARCHIVE_FOLDER}/segment--%Y-%m-%d--%H-%M-%S.mp4',
    format='segment',
    segment_time=3600,
    reset_timestamps=1,
    strftime=1,
    vcodec='copy',
    map='0:v'
)

hls_output = ffmpeg.output(
    input_stream,
    f'{LIVE_FOLDER}/live.m3u8',
    format='hls',
    hls_time=1,
    hls_list_size=3,
    hls_flags='delete_segments+independent_segments',
    vcodec='copy',
    map='0:v'
)

(
    ffmpeg.merge_outputs(archive_output, hls_output)
          .run(overwrite_output=True)
)
