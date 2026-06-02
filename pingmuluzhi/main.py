import customtkinter as ctk
from tkinter import filedialog, messagebox, Listbox, Scrollbar
import os
import json
import subprocess
import threading
import time
import cv2
import numpy as np

from recorder import ScreenRecorder
from audio_capturer import AudioCapturer
from annotator import AnnotationOverlay
from tray_icon import TrayIcon
from area_selector import AreaSelector
from video_compressor import VideoCompressor, generate_compressed_filename


class ScreenRecorderApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title("屏幕录制工具")
        self.root.geometry("400x500")
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.settings = self.load_settings()
        
        self.recorder = None
        self.audio_capturer = None
        self.annotator = None
        self.tray_icon = None
        
        self.is_recording = False
        self.is_paused = False
        
        self.record_mode = "fullscreen"
        self.custom_area = None
        
        self.duration = 0
        self.duration_label = None
        
        self.preview_label = None
        self.preview_thread = None
        
        self.recording_history = self.settings.get('last_recordings', [])
        
        self.init_ui()
        
        self.tray_icon = TrayIcon(
            on_show_main=self.show_main,
            on_stop=self.stop_recording,
            on_pause=self.pause_recording,
            on_resume=self.resume_recording
        )
        self.tray_icon.start()
    
    def load_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'save_path': '',
            'fps': 30,
            'quality': 'high',
            'record_cursor': True,
            'record_microphone': True,
            'record_system_audio': False,
            'last_recordings': [],
            'ask_compress': True
        }
    
    def save_settings(self):
        with open("settings.json", 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4)
    
    def init_ui(self):
        self.tab_view = ctk.CTkTabview(self.root, width=380, height=480)
        self.tab_view.pack(pady=10)
        
        self.tab_view.add("录制")
        self.tab_view.add("设置")
        self.tab_view.add("历史")
        
        self.init_recording_tab()
        self.init_settings_tab()
        self.init_history_tab()
    
    def init_recording_tab(self):
        tab = self.tab_view.tab("录制")
        
        mode_frame = ctk.CTkFrame(tab)
        mode_frame.pack(pady=10, padx=10, fill="x")
        
        mode_label = ctk.CTkLabel(mode_frame, text="录制模式")
        mode_label.pack(pady=5)
        
        self.mode_var = ctk.StringVar(value="fullscreen")
        
        mode_radio_full = ctk.CTkRadioButton(mode_frame, text="全屏录制", 
                                            variable=self.mode_var, value="fullscreen")
        mode_radio_full.pack(side="left", padx=10)
        
        mode_radio_window = ctk.CTkRadioButton(mode_frame, text="窗口录制", 
                                              variable=self.mode_var, value="window")
        mode_radio_window.pack(side="left", padx=10)
        
        mode_radio_custom = ctk.CTkRadioButton(mode_frame, text="自定义区域", 
                                               variable=self.mode_var, value="custom",
                                               command=self.select_custom_area)
        mode_radio_custom.pack(side="left", padx=10)
        
        self.custom_area_label = ctk.CTkLabel(mode_frame, text="")
        self.custom_area_label.pack(pady=5)
        
        preview_frame = ctk.CTkFrame(tab)
        preview_frame.pack(pady=10, padx=10, fill="x")
        
        preview_label = ctk.CTkLabel(preview_frame, text="实时预览")
        preview_label.pack(pady=5)
        
        self.preview_canvas = ctk.CTkCanvas(preview_frame, width=320, height=180, bg="black")
        self.preview_canvas.pack(pady=5)
        
        self.duration_label = ctk.CTkLabel(tab, text="录制时长: 00:00", font=("Arial", 16))
        self.duration_label.pack(pady=10)
        
        control_frame = ctk.CTkFrame(tab)
        control_frame.pack(pady=10, padx=10, fill="x")
        
        self.start_btn = ctk.CTkButton(control_frame, text="开始录制", 
                                      command=self.start_recording, width=80)
        self.start_btn.pack(side="left", padx=5)
        
        self.pause_btn = ctk.CTkButton(control_frame, text="暂停", 
                                      command=self.pause_recording, width=80, state="disabled")
        self.pause_btn.pack(side="left", padx=5)
        
        self.resume_btn = ctk.CTkButton(control_frame, text="继续", 
                                       command=self.resume_recording, width=80, state="disabled")
        self.resume_btn.pack(side="left", padx=5)
        
        self.stop_btn = ctk.CTkButton(control_frame, text="停止", 
                                     command=self.stop_recording, width=80, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
    
    def init_settings_tab(self):
        tab = self.tab_view.tab("设置")
        
        fps_frame = ctk.CTkFrame(tab)
        fps_frame.pack(pady=10, padx=10, fill="x")
        
        fps_label = ctk.CTkLabel(fps_frame, text="帧率")
        fps_label.pack(pady=5)
        
        self.fps_var = ctk.IntVar(value=self.settings.get('fps', 30))
        fps_options = [15, 24, 30, 60]
        fps_menu = ctk.CTkOptionMenu(fps_frame, variable=self.fps_var, values=[str(f) for f in fps_options])
        fps_menu.pack(pady=5)
        
        quality_frame = ctk.CTkFrame(tab)
        quality_frame.pack(pady=10, padx=10, fill="x")
        
        quality_label = ctk.CTkLabel(quality_frame, text="画质")
        quality_label.pack(pady=5)
        
        self.quality_var = ctk.StringVar(value=self.settings.get('quality', 'high'))
        quality_options = ["low", "medium", "high"]
        quality_menu = ctk.CTkOptionMenu(quality_frame, variable=self.quality_var, values=quality_options)
        quality_menu.pack(pady=5)
        
        cursor_frame = ctk.CTkFrame(tab)
        cursor_frame.pack(pady=10, padx=10, fill="x")
        
        self.cursor_var = ctk.BooleanVar(value=self.settings.get('record_cursor', True))
        cursor_check = ctk.CTkCheckBox(cursor_frame, text="录制鼠标光标", variable=self.cursor_var)
        cursor_check.pack(pady=5)
        
        mic_frame = ctk.CTkFrame(tab)
        mic_frame.pack(pady=10, padx=10, fill="x")
        
        self.mic_var = ctk.BooleanVar(value=self.settings.get('record_microphone', True))
        mic_check = ctk.CTkCheckBox(mic_frame, text="录制麦克风声音", variable=self.mic_var)
        mic_check.pack(pady=5)
        
        save_path_frame = ctk.CTkFrame(tab)
        save_path_frame.pack(pady=10, padx=10, fill="x")
        
        save_path_label = ctk.CTkLabel(save_path_frame, text="保存路径")
        save_path_label.pack(pady=5)
        
        self.save_path_entry = ctk.CTkEntry(save_path_frame, width=250)
        self.save_path_entry.insert(0, self.settings.get('save_path', ''))
        self.save_path_entry.pack(side="left", padx=5)
        
        browse_btn = ctk.CTkButton(save_path_frame, text="浏览", command=self.browse_save_path, width=60)
        browse_btn.pack(side="left", padx=5)
        
        compress_frame = ctk.CTkFrame(tab)
        compress_frame.pack(pady=10, padx=10, fill="x")
        
        self.ask_compress_var = ctk.BooleanVar(value=self.settings.get('ask_compress', True))
        compress_check = ctk.CTkCheckBox(compress_frame, text="录制完成后询问是否压缩", variable=self.ask_compress_var)
        compress_check.pack(pady=5)
        
        save_settings_btn = ctk.CTkButton(tab, text="保存设置", command=self.save_settings_action)
        save_settings_btn.pack(pady=10)
    
    def init_history_tab(self):
        tab = self.tab_view.tab("历史")
        
        history_label = ctk.CTkLabel(tab, text="录制历史")
        history_label.pack(pady=5)
        
        history_frame = ctk.CTkFrame(tab)
        history_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.history_listbox = Listbox(history_frame, bg="#2a2a2a", fg="white", 
                                      selectbackground="#1f6aa5", width=50)
        self.history_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = Scrollbar(history_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_listbox.yview)
        
        for recording in self.recording_history:
            self.history_listbox.insert("end", recording['name'])
        
        action_frame = ctk.CTkFrame(tab)
        action_frame.pack(pady=10, padx=10, fill="x")
        
        preview_btn = ctk.CTkButton(action_frame, text="预览", command=self.preview_recording, width=80)
        preview_btn.pack(side="left", padx=5)
        
        open_folder_btn = ctk.CTkButton(action_frame, text="打开文件夹", 
                                       command=self.open_recording_folder, width=100)
        open_folder_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(action_frame, text="删除", command=self.delete_recording, 
                                  width=80, fg_color="red", hover_color="#c0392b")
        delete_btn.pack(side="left", padx=5)
    
    def browse_save_path(self):
        path = filedialog.askdirectory()
        if path:
            self.save_path_entry.delete(0, "end")
            self.save_path_entry.insert(0, path)
    
    def save_settings_action(self):
        self.settings['fps'] = self.fps_var.get()
        self.settings['quality'] = self.quality_var.get()
        self.settings['record_cursor'] = self.cursor_var.get()
        self.settings['record_microphone'] = self.mic_var.get()
        self.settings['save_path'] = self.save_path_entry.get()
        self.settings['ask_compress'] = self.ask_compress_var.get()
        self.save_settings()
        messagebox.showinfo("提示", "设置已保存")
    
    def select_custom_area(self):
        self.root.iconify()
        
        def on_area_selected(area):
            self.custom_area = area
            self.custom_area_label.configure(text=f"区域: {area[0]},{area[1]} {area[2]}x{area[3]}")
            self.root.deiconify()
        
        selector = AreaSelector(on_select_callback=on_area_selected)
        selector.start()
    
    def start_recording(self):
        self.record_mode = self.mode_var.get()
        
        self.settings['fps'] = self.fps_var.get()
        self.settings['quality'] = self.quality_var.get()
        self.settings['record_cursor'] = self.cursor_var.get()
        self.settings['record_microphone'] = self.mic_var.get()
        self.settings['save_path'] = self.save_path_entry.get()
        self.save_settings()
        
        self.recorder = ScreenRecorder()
        self.audio_capturer = AudioCapturer()
        self.annotator = AnnotationOverlay()
        
        if self.record_mode == 'fullscreen':
            self.recorder.set_record_area('fullscreen')
        elif self.record_mode == 'window':
            self.recorder.set_record_area('window')
        elif self.record_mode == 'custom':
            if self.custom_area:
                self.recorder.set_record_area('custom', self.custom_area)
            else:
                self.recorder.set_record_area('fullscreen')
        
        self.recorder.start_recording()
        self.audio_capturer.start_recording()
        self.annotator.start()
        
        self.is_recording = True
        self.is_paused = False
        
        self.start_btn.configure(state="disabled")
        self.pause_btn.configure(state="normal")
        self.stop_btn.configure(state="normal")
        
        self.tray_icon.set_recording(True)
        self.tray_icon.set_paused(False)
        
        self.root.iconify()
        
        self.duration = 0
        self.update_duration()
        
        self.start_preview()
    
    def pause_recording(self):
        if self.recorder:
            self.recorder.pause_recording()
        if self.audio_capturer:
            self.audio_capturer.pause_recording()
        if self.annotator:
            self.annotator.pause()
        
        self.is_paused = True
        
        self.pause_btn.configure(state="disabled")
        self.resume_btn.configure(state="normal")
        
        self.tray_icon.set_paused(True)
    
    def resume_recording(self):
        if self.recorder:
            self.recorder.resume_recording()
        if self.audio_capturer:
            self.audio_capturer.resume_recording()
        if self.annotator:
            self.annotator.resume()
        
        self.is_paused = False
        
        self.pause_btn.configure(state="normal")
        self.resume_btn.configure(state="disabled")
        
        self.tray_icon.set_paused(False)
    
    def stop_recording(self):
        if self.recorder:
            video_path = self.recorder.stop_recording()
        if self.audio_capturer:
            self.audio_capturer.stop_recording()
        if self.annotator:
            self.annotator.stop()
        
        self.is_recording = False
        
        self.start_btn.configure(state="normal")
        self.pause_btn.configure(state="disabled")
        self.resume_btn.configure(state="disabled")
        self.stop_btn.configure(state="disabled")
        
        self.tray_icon.set_recording(False)
        self.tray_icon.set_paused(False)
        
        if self.preview_thread:
            self.preview_thread = None
        
        self.root.deiconify()
        
        if video_path and os.path.exists(video_path):
            recording_name = os.path.basename(video_path)
            self.recording_history.insert(0, {
                'name': recording_name,
                'path': video_path,
                'time': time.strftime("%Y-%m-%d %H:%M:%S")
            })
            if len(self.recording_history) > 20:
                self.recording_history = self.recording_history[:20]
            
            self.settings['last_recordings'] = self.recording_history
            self.save_settings()
            
            self.history_listbox.insert(0, recording_name)
            
            messagebox.showinfo("提示", f"录制完成！\n文件已保存到:\n{video_path}")
            
            self.check_compress_video(video_path)
    
    def check_compress_video(self, video_path):
        if not self.settings.get('ask_compress', True):
            return
        
        result = self.show_compress_dialog()
        if result == "light":
            self.start_compression(video_path, "light")
        elif result == "medium":
            self.start_compression(video_path, "medium")
    
    def show_compress_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("视频压缩")
        dialog.geometry("300x200")
        dialog.attributes("-topmost", True)
        
        label = ctk.CTkLabel(dialog, text="是否对刚刚录制的视频进行压缩？")
        label.pack(pady=10)
        
        var = ctk.StringVar(value="none")
        
        none_btn = ctk.CTkRadioButton(dialog, text="不压缩", variable=var, value="none")
        none_btn.pack(pady=5)
        
        light_btn = ctk.CTkRadioButton(dialog, text="轻度压缩（降低码率约30%，画质基本无损）", variable=var, value="light")
        light_btn.pack(pady=5)
        
        medium_btn = ctk.CTkRadioButton(dialog, text="中度压缩（分辨率缩放到720p，帧率降为原一半）", variable=var, value="medium")
        medium_btn.pack(pady=5)
        
        confirm_btn = ctk.CTkButton(dialog, text="确定", command=dialog.destroy)
        confirm_btn.pack(pady=10)
        
        dialog.grab_set()
        self.root.wait_window(dialog)
        
        return var.get()
    
    def start_compression(self, input_path, level):
        output_path = generate_compressed_filename(input_path)
        
        self.progress_dialog = ctk.CTkToplevel(self.root)
        self.progress_dialog.title("压缩进度")
        self.progress_dialog.geometry("300x120")
        self.progress_dialog.attributes("-topmost", True)
        
        self.progress_label = ctk.CTkLabel(self.progress_dialog, text="正在压缩...")
        self.progress_label.pack(pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_dialog, width=250)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)
        
        self.cancel_btn = ctk.CTkButton(self.progress_dialog, text="取消", command=self.cancel_compression)
        self.cancel_btn.pack(pady=5)
        
        self.compressor = VideoCompressor()
        self.compressor.compress_video(
            input_path,
            output_path,
            level,
            progress_callback=self.update_compression_progress,
            complete_callback=self.on_compression_complete
        )
        
        self.progress_dialog.grab_set()
    
    def update_compression_progress(self, progress):
        if self.progress_dialog and self.progress_bar and self.progress_label:
            try:
                self.root.after(0, lambda: self._update_progress_ui(progress))
            except:
                pass
    
    def _update_progress_ui(self, progress):
        try:
            if self.progress_bar and self.progress_label:
                self.progress_bar.set(progress / 100)
                self.progress_label.configure(text=f"正在压缩... {progress}%")
        except:
            pass
    
    def cancel_compression(self):
        if self.compressor:
            self.compressor.cancel()
        if self.progress_dialog:
            try:
                self.progress_dialog.destroy()
            except:
                pass
            self.progress_dialog = None
            self.progress_bar = None
            self.progress_label = None
    
    def on_compression_complete(self, success, error_message):
        self.root.after(0, lambda: self._on_compression_complete_ui(success, error_message))
    
    def _on_compression_complete_ui(self, success, error_message):
        if self.progress_dialog:
            try:
                self.progress_dialog.destroy()
            except:
                pass
            self.progress_dialog = None
            self.progress_bar = None
            self.progress_label = None
        
        if success:
            try:
                output_path = generate_compressed_filename(self.recorder.video_path)
                
                original_size = os.path.getsize(self.recorder.video_path)
                compressed_size = os.path.getsize(output_path)
                compression_ratio = (1 - compressed_size / original_size) * 100
                
                self.show_compress_result_dialog(output_path, original_size, compressed_size, compression_ratio)
                
                compressed_name = os.path.basename(output_path)
                self.recording_history.insert(0, {
                    'name': f"[压缩版] {compressed_name}",
                    'path': output_path,
                    'time': time.strftime("%Y-%m-%d %H:%M:%S")
                })
                if len(self.recording_history) > 20:
                    self.recording_history = self.recording_history[:20]
                
                self.settings['last_recordings'] = self.recording_history
                self.save_settings()
                
                self.history_listbox.insert(0, f"[压缩版] {compressed_name}")
            except Exception as e:
                messagebox.showerror("压缩失败", f"处理压缩结果时出错:\n{str(e)}")
        else:
            if error_message != "压缩已取消":
                messagebox.showerror("压缩失败", f"压缩过程中发生错误:\n{error_message}")
    
    def show_compress_result_dialog(self, output_path, original_size, compressed_size, ratio):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("压缩完成")
        dialog.geometry("350x200")
        dialog.attributes("-topmost", True)
        
        original_size_str = self.format_file_size(original_size)
        compressed_size_str = self.format_file_size(compressed_size)
        
        label1 = ctk.CTkLabel(dialog, text=f"原文件大小: {original_size_str}")
        label1.pack(pady=5)
        
        label2 = ctk.CTkLabel(dialog, text=f"压缩后大小: {compressed_size_str}")
        label2.pack(pady=5)
        
        label3 = ctk.CTkLabel(dialog, text=f"压缩率: {ratio:.1f}%")
        label3.pack(pady=10)
        
        frame = ctk.CTkFrame(dialog)
        frame.pack(pady=5)
        
        open_folder_btn = ctk.CTkButton(frame, text="打开文件夹", command=lambda: self.open_compressed_folder(output_path))
        open_folder_btn.pack(side="left", padx=5)
        
        play_btn = ctk.CTkButton(frame, text="播放压缩版", command=lambda: self.play_compressed_video(output_path))
        play_btn.pack(side="left", padx=5)
        
        dialog.grab_set()
    
    def format_file_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    def open_compressed_folder(self, file_path):
        folder = os.path.dirname(file_path)
        subprocess.run(['explorer', folder], shell=True)
    
    def play_compressed_video(self, file_path):
        if os.path.exists(file_path):
            subprocess.run(['start', file_path], shell=True)
    
    def update_duration(self):
        if self.is_recording and not self.is_paused:
            self.duration += 1
            mins = self.duration // 60
            secs = self.duration % 60
            self.duration_label.configure(text=f"录制时长: {mins:02d}:{secs:02d}")
        
        if self.is_recording:
            self.root.after(1000, self.update_duration)
    
    def start_preview(self):
        def preview_loop():
            while self.is_recording:
                if self.recorder and self.recorder.frame_queue.qsize() > 0:
                    frame = self.recorder.frame_queue.queue[-1]
                    frame = cv2.resize(frame, (320, 180))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    img = ctk.CTkImage(light_image=None, dark_image=frame, size=(320, 180))
                    self.preview_canvas.delete("all")
                    self.preview_canvas.create_image(0, 0, image=img, anchor="nw")
                
                time.sleep(0.1)
        
        self.preview_thread = threading.Thread(target=preview_loop)
        self.preview_thread.daemon = True
        self.preview_thread.start()
    
    def preview_recording(self):
        selected = self.history_listbox.curselection()
        if selected:
            index = selected[0]
            recording = self.recording_history[index]
            if os.path.exists(recording['path']):
                subprocess.run(['start', recording['path']], shell=True)
            else:
                messagebox.showwarning("警告", "文件不存在")
    
    def open_recording_folder(self):
        selected = self.history_listbox.curselection()
        if selected:
            index = selected[0]
            recording = self.recording_history[index]
            folder = os.path.dirname(recording['path'])
            subprocess.run(['explorer', folder], shell=True)
    
    def delete_recording(self):
        selected = self.history_listbox.curselection()
        if selected:
            index = selected[0]
            recording = self.recording_history[index]
            
            if messagebox.askyesno("确认删除", f"确定要删除 {recording['name']} 吗？"):
                if os.path.exists(recording['path']):
                    os.remove(recording['path'])
                
                del self.recording_history[index]
                self.history_listbox.delete(index)
                
                self.settings['last_recordings'] = self.recording_history
                self.save_settings()
    
    def show_main(self):
        self.root.deiconify()
        self.root.lift()
    
    def on_close(self):
        if self.is_recording:
            if messagebox.askyesno("确认退出", "正在录制中，确定要退出吗？"):
                self.stop_recording()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ScreenRecorderApp()
    app.run()