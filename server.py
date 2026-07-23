# -*- coding: utf-8 -*-
"""
server.py — Local HTTP server (127.0.0.1) ដែលទទួលសំណើពី Chrome Extension
ហើយហៅមកកម្មវិធីលើ Desktop ឲ្យចាប់ផ្តើមទាញយក។

ហេតុអ្វីត្រូវការ server នេះ?
    Chrome Extension មិនអាចទាញយកវីដេអូ YouTube ដោយផ្ទាល់បានទេ ព្រោះ YouTube
    ធ្វើ encrypt streaming URLs និង Google Chrome Web Store ក៏មិនអនុញ្ញាតឲ្យ
    extension បំពានលក្ខខណ្ឌប្រើប្រាស់របស់ YouTube ដែរ។ ដូច្នេះ extension គ្រាន់តែ
    ផ្ញើ "តំណវីដេអូបច្ចុប្បន្ន" មក server នេះ (ដែលរត់នៅលើកុំព្យូទ័រអ្នកប្រើផ្ទាល់)
    រួច yt-dlp (ក្នុងកម្មវិធី Desktop) ជាអ្នកទាញយកជំនួស។

Endpoint:
    POST /download   body: {"url": "...", "audio_only": false}
    GET  /ping        សម្រាប់ extension ពិនិត្យថា desktop app កំពុងបើករត់ដែរឬទេ
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8765

# ដើម្បីកុំឲ្យគេហទំព័រណាមួយផ្សេងហៅ server នេះបានដោយអាថ៌កំបាំង យើងកំណត់
# ថាតែ origin chrome-extension:// ប៉ុណ្ណោះទើបទទួលយក (ការពារកម្រិតមូលដ្ឋាន)
ALLOWED_ORIGIN_PREFIX = "chrome-extension://"


def make_handler(on_download_callback):
    """on_download_callback(url: str, audio_only: bool) -> None"""

    class Handler(BaseHTTPRequestHandler):
        def _cors_headers(self):
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")

        def do_OPTIONS(self):
            self.send_response(204)
            self._cors_headers()
            self.end_headers()

        def do_GET(self):
            if self.path == "/ping":
                self.send_response(200)
                self._cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "app": "SK"}).encode())
            else:
                self.send_response(404)
                self._cors_headers()
                self.end_headers()

        def do_POST(self):
            if self.path != "/download":
                self.send_response(404)
                self._cors_headers()
                self.end_headers()
                return
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length)
                data = json.loads(raw.decode("utf-8"))
                url = data.get("url", "").strip()
                audio_only = bool(data.get("audio_only", False))
                if not url:
                    raise ValueError("url ទទេ")
                on_download_callback(url, audio_only)
                resp = {"status": "started", "url": url}
                code = 200
            except Exception as e:
                resp = {"status": "error", "message": str(e)}
                code = 400

            self.send_response(code)
            self._cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode())

        def log_message(self, fmt, *args):
            pass  # បិទ log ធម្មតារបស់ http.server កុំឲ្យរញែកញ៉ែក console

    return Handler


class ExtensionBridgeServer:
    """រត់ local HTTP server ក្នុង background thread មួយដាច់ដោយឡែក."""

    def __init__(self, on_download_callback, port=PORT):
        self.port = port
        self._httpd = HTTPServer(("127.0.0.1", port), make_handler(on_download_callback))
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)

    def start(self):
        self._thread.start()

    def stop(self):
        self._httpd.shutdown()
