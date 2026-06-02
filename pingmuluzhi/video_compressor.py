import os
import threading
import time
import cv2


class VideoCompressor:
    def __init__(self):
        self.process = None
        self.is_cancelled = False
        self.compression_thread = None
        self.progress_callback = None
        self.complete_callback = None

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

            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                if self.complete_callback:
                    self.complete_callback(False, "无法打开视频文件")
                return

            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            if fps <= 0:
                fps = 30

            if compression_level == "medium":
                new_width = 1280
                new_height = 720
                target_fps = 15
            else:
                new_width = width
                new_height = height
                target_fps = fps

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            
            out = cv2.VideoWriter(output_path, fourcc, target_fps, (new_width, new_height))

            frame_count = 0
            last_report_time = 0
            
            while cap.isOpened():
                if self.is_cancelled:
                    cap.release()
                    out.release()
                    if os.path.exists(output_path):
                        try:
                            os.remove(output_path)
                        except:
                            pass
                    if self.complete_callback:
                        self.complete_callback(False, "压缩已取消")
                    return

                ret, frame = cap.read()
                if not ret:
                    break

                if compression_level == "medium":
                    frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

                if compression_level == "medium" and target_fps != fps:
                    if frame_count % int(fps / target_fps) == 0:
                        out.write(frame)
                else:
                    out.write(frame)

                frame_count += 1
                current_time = time.time()
                
                if total_frames > 0 and current_time - last_report_time > 0.1:
                    progress = min(100, int((frame_count / total_frames) * 100))
                    if self.progress_callback:
                        self.progress_callback(progress)
                    last_report_time = current_time

            cap.release()
            out.release()

            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                if self.progress_callback:
                    self.progress_callback(100)
                if self.complete_callback:
                    self.complete_callback(True, None)
            else:
                if self.complete_callback:
                    self.complete_callback(False, "压缩失败，无法生成输出文件")

        except Exception as e:
            if self.complete_callback:
                self.complete_callback(False, str(e))

    def cancel(self):
        self.is_cancelled = True

    def is_running(self):
        return self.compression_thread is not None and self.compression_thread.is_alive()


def generate_compressed_filename(input_path):
    dir_name = os.path.dirname(input_path)
    base_name = os.path.basename(input_path)
    name_without_ext = os.path.splitext(base_name)[0]
    return os.path.join(dir_name, f"{name_without_ext}_压缩版.mp4")