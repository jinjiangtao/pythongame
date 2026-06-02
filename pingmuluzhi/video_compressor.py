import os
import subprocess
import threading
import time
import shutil


class VideoCompressor:
    def __init__(self):
        self.process = None
        self.is_cancelled = False
        self.compression_thread = None
        self.progress_callback = None
        self.complete_callback = None
        self.ffmpeg_path = self._find_ffmpeg()

    def _find_ffmpeg(self):
        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path:
            return ffmpeg_path
        
        common_paths = [
            "C:\\ffmpeg\\bin\\ffmpeg.exe",
            "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
            "C:\\Program Files (x86)\\ffmpeg\\bin\\ffmpeg.exe",
            os.path.join(os.path.dirname(__file__), "ffmpeg.exe")
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return "ffmpeg"

    def compress_video(self, input_path, output_path, compression_level, progress_callback=None, complete_callback=None):
        self.progress_callback = progress_callback
        self.complete_callback = complete_callback
        self.is_cancelled = False

        self.compression_thread = threading.Thread(
            target=self._compress_worker,
            args=(input_path, output_path, compression_level)
        )
        self.compression_thread.start()

    def _compress_worker(self, input_path, output_path, compression_level):
        try:
            if not os.path.exists(input_path):
                if self.complete_callback:
                    self.complete_callback(False, f"输入文件不存在: {input_path}")
                return

            if not self.ffmpeg_path:
                if self.complete_callback:
                    self.complete_callback(False, "未找到 ffmpeg，请先安装 ffmpeg 并添加到系统 PATH")
                return

            ffmpeg_cmd = self._build_ffmpeg_command(input_path, output_path, compression_level)
            
            self.process = subprocess.Popen(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                shell=True
            )

            total_duration = self._get_video_duration(input_path)
            
            for line in self.process.stdout:
                if self.is_cancelled:
                    self._terminate_process()
                    if self.complete_callback:
                        self.complete_callback(False, "压缩已取消")
                    return

                progress = self._parse_progress(line, total_duration)
                if progress is not None and self.progress_callback:
                    self.progress_callback(progress)

            self.process.wait()

            if self.process.returncode == 0 and os.path.exists(output_path):
                if self.complete_callback:
                    self.complete_callback(True, None)
            else:
                error_msg = f"压缩失败，返回码: {self.process.returncode}"
                if self.process.returncode == 1:
                    error_msg = "压缩失败，请检查 ffmpeg 是否正确安装"
                elif self.process.returncode == -1073741515:
                    error_msg = "ffmpeg 执行被中断"
                if self.complete_callback:
                    self.complete_callback(False, error_msg)

        except FileNotFoundError:
            if self.complete_callback:
                self.complete_callback(False, "未找到 ffmpeg 可执行文件，请安装 ffmpeg 并添加到系统 PATH")
        except Exception as e:
            if self.complete_callback:
                self.complete_callback(False, str(e))
        finally:
            self.process = None

    def _build_ffmpeg_command(self, input_path, output_path, compression_level):
        cmd = f'"{self.ffmpeg_path}" -i "{input_path}" -y'

        if compression_level == "light":
            cmd += ' -c:v libx264 -crf 23 -c:a aac -b:a 128k'
        elif compression_level == "medium":
            cmd += ' -c:v libx264 -crf 23 -vf scale=1280:720 -r 15 -c:a aac -b:a 128k'

        cmd += f' "{output_path}"'
        return cmd

    def _get_video_duration(self, input_path):
        try:
            result = subprocess.run(
                f'"{self.ffmpeg_path}" -i "{input_path}"',
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True,
                shell=True
            )
            for line in result.stderr.split('\n'):
                if "Duration:" in line:
                    parts = line.split(',')[0].split(' ')[1]
                    h, m, s = parts.split(':')
                    return float(h) * 3600 + float(m) * 60 + float(s)
        except:
            pass
        return 1.0

    def _parse_progress(self, line, total_duration):
        if "time=" in line:
            try:
                time_str = line.split("time=")[1].split(' ')[0]
                h, m, s = time_str.split(':')
                current_time = float(h) * 3600 + float(m) * 60 + float(s)
                if total_duration > 0:
                    return min(100, int((current_time / total_duration) * 100))
            except:
                pass
        return None

    def _terminate_process(self):
        if self.process:
            try:
                self.process.terminate()
                time.sleep(0.5)
                if self.process.poll() is None:
                    self.process.kill()
            except:
                pass

    def cancel(self):
        self.is_cancelled = True

    def is_running(self):
        return self.compression_thread is not None and self.compression_thread.is_alive()


def generate_compressed_filename(input_path):
    dir_name = os.path.dirname(input_path)
    base_name = os.path.basename(input_path)
    name_without_ext = os.path.splitext(base_name)[0]
    return os.path.join(dir_name, f"{name_without_ext}_压缩版.mp4")