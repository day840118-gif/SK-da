#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SK — កម្មវិធីទាញយកវីដេអូ YouTube (ស្រដៀង IDM)
មានប្រព័ន្ធ Activation Key + ភ្ជាប់ជាមួយ Chrome Extension

តម្រូវការ:
    pip install -r requirements.txt
    ដំឡើង FFmpeg (សម្រាប់ merge គុណភាពខ្ពស់ និង MP3)

រត់:
    python yt_downloader_pro.py
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import license as lic
from server import ExtensionBridgeServer

try:
    import yt_dlp
except ImportError:
    print("yt-dlp មិនទាន់បានដំឡើងទេ។ សូមរត់: pip install -r requirements.txt")
    sys.exit(1)


APP_TITLE = "SK"
BRIDGE_PORT = 8765


# ======================================================================
#  ACTIVATION WINDOW
# ======================================================================
class ActivationDialog(tk.Toplevel):
    """បង្អួចសុំលេខ Activation Key មុនប្រើកម្មវិធី."""

    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success
        self.title(f"{APP_TITLE} — Activation")
        self.geometry("460x260")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.grab_set()  # modal

        pad = {"padx": 20, "pady": 8}
        ttk.Label(self, text="🔑 សូមបញ្ចូល Activation Key", font=("Segoe UI", 13, "bold")
                  ).pack(**pad)
        ttk.Label(self, text="ទម្រង់: XXXXX-XXXXX-XXXXX-XXXXX", foreground="#a6adc8"
                  ).pack()

        self.key_var = tk.StringVar()
        entry = ttk.Entry(self, textvariable=self.key_var, font=("Consolas", 13),
                           justify="center", width=30)
        entry.pack(pady=16)
        entry.focus()
        entry.bind("<Return>", lambda e: self._activate())

        self.msg_lbl = ttk.Label(self, text="", foreground="#f38ba8")
        self.msg_lbl.pack()

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="✔ ធ្វើ Activate", command=self._activate
                   ).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="ចាកចេញ", command=self._on_close
                   ).pack(side="left", padx=6)

    def _activate(self):
        key = self.key_var.get().strip()
        if lic.activate(key):
            self.destroy()
            self.on_success()
        else:
            self.msg_lbl.config(text="❌ Key មិនត្រឹមត្រូវទេ សូមពិនិត្យម្តងទៀត។")

    def _on_close(self):
        self.destroy()
        self.master.destroy()


# ======================================================================
#  MAIN APP
# ======================================================================
class YTDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()  # hide until activated
        self.title(APP_TITLE)
        self.geometry("780x600")
        self.minsize(700, 520)
        self.configure(bg="#1e1e2e")

        self.video_info = None
        self.format_map = {}
        self.output_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        self.cancel_flag = threading.Event()
        self.bridge = None

        if lic.is_activated():
            self._init_main_ui()
            self.deiconify()
        else:
            ActivationDialog(self, on_success=self._on_activated)

    def _on_activated(self):
        self.title(f"{APP_TITLE}  —  Activated")
        self._init_main_ui()
        self.deiconify()

    def _init_main_ui(self):
        self._build_style()
        self._build_ui()
        self._start_bridge_server()

    # ---------------------------------------------------------- STYLE --
    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        bg, fg, accent = "#1e1e2e", "#cdd6f4", "#89b4fa"
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground=accent)
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("Horizontal.TProgressbar", troughcolor="#313244",
                         background=accent, thickness=18)

    # ---------------------------------------------------------- UI ------
    def _build_ui(self):
        pad = {"padx": 12, "pady": 6}

        top = ttk.Frame(self)
        top.pack(fill="x", **pad)
        ttk.Label(top, text="SK", style="Title.TLabel").pack(side="left")
        self.bridge_status_lbl = ttk.Label(top, text="🔌 Extension Bridge: កំពុងចាប់ផ្តើម...",
                                            foreground="#a6adc8")
        self.bridge_status_lbl.pack(side="right")

        url_frame = ttk.Frame(self)
        url_frame.pack(fill="x", **pad)
        ttk.Label(url_frame, text="តំណវីដេអូ (URL):").pack(side="left")
        self.url_var = tk.StringVar()
        ttk.Entry(url_frame, textvariable=self.url_var, font=("Segoe UI", 10)
                  ).pack(side="left", fill="x", expand=True, padx=8)
        self.fetch_btn = ttk.Button(url_frame, text="ទាញយកព័ត៌មាន", command=self.on_fetch_info)
        self.fetch_btn.pack(side="left")

        info_frame = ttk.Frame(self)
        info_frame.pack(fill="x", **pad)
        self.title_lbl = ttk.Label(info_frame, text="", wraplength=720, justify="left")
        self.title_lbl.pack(anchor="w")

        fmt_frame = ttk.Frame(self)
        fmt_frame.pack(fill="x", **pad)
        ttk.Label(fmt_frame, text="គុណភាព / Format:").pack(side="left")
        self.format_var = tk.StringVar()
        self.format_combo = ttk.Combobox(fmt_frame, textvariable=self.format_var,
                                          state="readonly", width=55)
        self.format_combo.pack(side="left", padx=8, fill="x", expand=True)
        self.audio_only_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(fmt_frame, text="សំឡេងតែប៉ុណ្ណោះ (MP3)", variable=self.audio_only_var,
                         command=self._toggle_audio_only).pack(side="left", padx=8)

        out_frame = ttk.Frame(self)
        out_frame.pack(fill="x", **pad)
        ttk.Label(out_frame, text="ទីតាំងរក្សាទុក:").pack(side="left")
        self.out_var = tk.StringVar(value=self.output_dir)
        ttk.Entry(out_frame, textvariable=self.out_var).pack(side="left", fill="x", expand=True, padx=8)
        ttk.Button(out_frame, text="ជ្រើសរើស...", command=self.on_choose_folder).pack(side="left")

        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", **pad)
        self.download_btn = ttk.Button(action_frame, text="⬇ ចាប់ផ្តើមទាញយក", command=self.on_download)
        self.download_btn.pack(side="left")
        self.cancel_btn = ttk.Button(action_frame, text="បោះបង់", command=self.on_cancel, state="disabled")
        self.cancel_btn.pack(side="left", padx=8)

        prog_frame = ttk.Frame(self)
        prog_frame.pack(fill="x", **pad)
        self.progress = ttk.Progressbar(prog_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x")
        self.status_lbl = ttk.Label(prog_frame, text="ត្រៀមរួចរាល់ / Ready")
        self.status_lbl.pack(anchor="w", pady=(4, 0))

        log_frame = ttk.Frame(self)
        log_frame.pack(fill="both", expand=True, **pad)
        ttk.Label(log_frame, text="កំណត់ហេតុ (Log):").pack(anchor="w")
        self.log_box = tk.Text(log_frame, height=10, bg="#181825", fg="#a6adc8",
                                insertbackground="#cdd6f4", font=("Consolas", 9), relief="flat")
        self.log_box.pack(fill="both", expand=True)

    # ---------------------------------------------------------- HELPERS --
    def log(self, msg):
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")

    def set_status(self, msg):
        self.status_lbl.config(text=msg)

    def _toggle_audio_only(self):
        self.format_combo.config(state="disabled" if self.audio_only_var.get() else "readonly")

    def on_choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.output_dir)
        if folder:
            self.output_dir = folder
            self.out_var.set(folder)

    # ---------------------------------------------------------- BRIDGE SERVER --
    def _start_bridge_server(self):
        try:
            self.bridge = ExtensionBridgeServer(self._handle_extension_request, port=BRIDGE_PORT)
            self.bridge.start()
            self.bridge_status_lbl.config(
                text=f"🟢 Extension Bridge: ដំណើរការនៅ port {BRIDGE_PORT}")
        except OSError:
            self.bridge_status_lbl.config(text="🔴 Extension Bridge: port កំពុងជាប់ រកមិនឃើញ")

    def _handle_extension_request(self, url, audio_only):
        """ហៅពី server thread ពេល Chrome Extension ផ្ញើសំណើមក."""
        self.after(0, self._start_extension_download, url, audio_only)

    def _start_extension_download(self, url, audio_only):
        self.url_var.set(url)
        self.audio_only_var.set(audio_only)
        self._toggle_audio_only()
        self.log(f"📥 ទទួលសំណើពី Chrome Extension: {url}")
        os.makedirs(self.out_var.get(), exist_ok=True)
        self.cancel_flag.clear()
        self.download_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.progress["value"] = 0
        self.set_status("កំពុងទាញយកពី Extension...")
        threading.Thread(target=self._download_worker, args=(url, "best"), daemon=True).start()

    # ---------------------------------------------------------- FETCH INFO --
    def on_fetch_info(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning(APP_TITLE, "សូមបញ្ចូលតំណវីដេអូជាមុនសិន។")
            return
        self.fetch_btn.config(state="disabled")
        self.set_status("កំពុងទាញយកព័ត៌មានវីដេអូ...")
        threading.Thread(target=self._fetch_info_worker, args=(url,), daemon=True).start()

    def _fetch_info_worker(self, url):
        try:
            with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "skip_download": True}) as ydl:
                info = ydl.extract_info(url, download=False)
            self.video_info = info
            self.after(0, self._populate_formats, info)
        except Exception as e:
            self.after(0, self._on_error, f"មិនអាចទាញយកព័ត៌មានបានទេ: {e}")
        finally:
            self.after(0, lambda: self.fetch_btn.config(state="normal"))

    def _populate_formats(self, info):
        title = info.get("title", "N/A")
        duration = info.get("duration", 0)
        mins, secs = divmod(int(duration or 0), 60)
        self.title_lbl.config(text=f"🎬 {title}  ({mins}:{secs:02d})")

        formats = info.get("formats", [])
        self.format_map.clear()
        display_list = []
        for f in formats:
            if f.get("vcodec") == "none":
                continue
            height = f.get("height")
            if not height:
                continue
            fps = f.get("fps")
            ext = f.get("ext")
            filesize = f.get("filesize") or f.get("filesize_approx")
            size_str = f"{filesize / (1024*1024):.1f}MB" if filesize else "?MB"
            acodec = f.get("acodec")
            has_audio = "🔊" if acodec and acodec != "none" else "🔇(no audio)"
            label = f"{height}p{int(fps) if fps else ''} - {ext} - {size_str} {has_audio}"
            self.format_map[label] = f.get("format_id")
            display_list.append((height, label))

        display_list.sort(key=lambda x: x[0], reverse=True)
        labels = [d[1] for d in display_list]
        self.format_combo["values"] = labels
        if labels:
            self.format_combo.current(0)
        self.set_status("ត្រៀមរួចរាល់ / Ready — ជ្រើសរើសគុណភាព រួចចុចទាញយក")
        self.log(f"បានរកឃើញ {len(labels)} ជម្រើសគុណភាព សម្រាប់: {title}")

    def _on_error(self, msg):
        self.set_status("មានបញ្ហា / Error")
        self.log("❌ " + msg)
        messagebox.showerror(APP_TITLE, msg)

    # ---------------------------------------------------------- DOWNLOAD --
    def on_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning(APP_TITLE, "សូមបញ្ចូលតំណវីដេអូជាមុនសិន។")
            return
        if not self.audio_only_var.get() and not self.format_var.get():
            messagebox.showwarning(APP_TITLE, "សូមទាញយកព័ត៌មាន និងជ្រើសរើសគុណភាពជាមុនសិន។")
            return

        os.makedirs(self.out_var.get(), exist_ok=True)
        self.cancel_flag.clear()
        self.download_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.progress["value"] = 0
        self.set_status("កំពុងទាញយក...")

        format_choice = self.format_map.get(self.format_var.get(), "best")
        threading.Thread(target=self._download_worker, args=(url, format_choice), daemon=True).start()

    def _progress_hook(self, d):
        if self.cancel_flag.is_set():
            raise yt_dlp.utils.DownloadError("បោះបង់ដោយអ្នកប្រើប្រាស់ / Cancelled by user")
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            speed = d.get("speed")
            eta = d.get("eta")
            pct = (downloaded / total * 100) if total else 0
            speed_str = f"{speed/1024/1024:.2f} MB/s" if speed else "?"
            eta_str = f"{eta}s" if eta is not None else "?"
            self.after(0, self._update_progress, pct, speed_str, eta_str)
        elif d["status"] == "finished":
            self.after(0, self.set_status, "កំពុងបញ្ចប់ (merging/processing)...")

    def _update_progress(self, pct, speed_str, eta_str):
        self.progress["value"] = pct
        self.set_status(f"កំពុងទាញយក {pct:.1f}%  |  ល្បឿន: {speed_str}  |  នៅសល់: {eta_str}")

    def _download_worker(self, url, format_choice):
        outtmpl = os.path.join(self.out_var.get(), "%(title)s.%(ext)s")
        if self.audio_only_var.get():
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": outtmpl,
                "progress_hooks": [self._progress_hook],
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "quiet": True,
                "no_warnings": True,
            }
        else:
            fmt = f"{format_choice}+bestaudio/best" if format_choice != "best" else "best"
            ydl_opts = {
                "format": fmt,
                "outtmpl": outtmpl,
                "progress_hooks": [self._progress_hook],
                "merge_output_format": "mp4",
                "quiet": True,
                "no_warnings": True,
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.after(0, self._on_download_done)
        except Exception as e:
            self.after(0, self._on_download_error, str(e))

    def _on_download_done(self):
        self.progress["value"] = 100
        self.set_status("✅ ទាញយករួចរាល់! / Download complete")
        self.log("✅ ការទាញយកបានបញ្ចប់ដោយជោគជ័យ។ រក្សាទុកនៅ: " + self.out_var.get())
        self.download_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")

    def _on_download_error(self, msg):
        self.set_status("❌ បរាជ័យ / Failed")
        self.log("❌ " + msg)
        self.download_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        if "Cancelled" not in msg:
            messagebox.showerror(APP_TITLE, f"ការទាញយកបានបរាជ័យ:\n{msg}")

    def on_cancel(self):
        self.cancel_flag.set()
        self.set_status("កំពុងបោះបង់...")


def main():
    app = YTDownloaderApp()
    app.mainloop()


if __name__ == "__main__":
    main()
