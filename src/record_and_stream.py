import ffmpeg
import os
import signal
import subprocess
from datetime import datetime, timedelta


class StreamRecorder:
    def __init__(self, rtsp_url, archive_folder, live_folder):
        self.rtsp_url = rtsp_url
        self.archive_folder = archive_folder
        self.live_folder = live_folder
        self.process = None
        self.recording_start_time = None
        self.current_file = None
        self.previous_file = None
        self.expected_duration = timedelta(hours=1)
        
        os.makedirs(self.archive_folder, exist_ok=True)
        os.makedirs(self.live_folder, exist_ok=True)

    def start_recording(self):
        """Start new recording"""
        self.stop_recording()
        
        self.recording_start_time = datetime.now()
        start_str = self.recording_start_time.strftime('%Y-%m-%d--%H-%M-%S')
        end_str = (self.recording_start_time + self.expected_duration).strftime('%Y-%m-%d--%H-%M-%S')
        
        self.current_file = f"from--{start_str}--to--{end_str}.mp4"
        file_path = os.path.join(self.archive_folder, self.current_file)
        
        input_stream = ffmpeg.input(
            self.rtsp_url,
            rtsp_transport='tcp',
            fflags='+genpts'
        )

        archive_output = ffmpeg.output(
            input_stream,
            file_path,
            format='segment',
            segment_time=3600,
            reset_timestamps=1,
            strftime=1,
            vcodec='copy',
            map='0:v'
        )

        hls_output = ffmpeg.output(
            input_stream,
            os.path.join(self.live_folder, 'live.m3u8'),
            format='hls',
            hls_time=1,
            hls_list_size=3,
            hls_flags='delete_segments+independent_segments',
            vcodec='copy',
            map='0:v'
        )

        cmd = ffmpeg.merge_outputs(archive_output, hls_output).compile()
        self.process = subprocess.Popen(cmd)
        self.recording_start_time = datetime.now()
        return True

    def stop_recording(self):
        """Stop recording and update end time if needed"""
        if self.process and self.process.poll() is None:
            self.process.send_signal(signal.SIGINT)
            try:
                self.process.wait(timeout=5)
                
                if self.current_file:
                    actual_end_time = datetime.now()
                    old_path = os.path.join(self.archive_folder, self.current_file)
                    
                    if os.path.exists(old_path):
                        parts = self.current_file.split('--')
                        start_str = parts[1] + '--' + parts[2]
                        
                        new_filename = f"from--{start_str}--to--{actual_end_time.strftime('%Y-%m-%d--%H-%M-%S')}.mp4"
                        new_path = os.path.join(self.archive_folder, new_filename)
                        
                        os.rename(old_path, new_path)
                        self.current_file = new_filename
                
                return True
            except subprocess.TimeoutExpired:
                self.process.terminate()
            except Exception as e:
                print(f"Error renaming file: {e}")
            finally:
                self.process = None
        return False

    def restart_recording(self):
        """Restart recording"""
        self.stop_recording()
        return self.start_recording()
