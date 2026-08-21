#!/usr/bin/env python3
"""Dev server that never lets the browser cache — local preview only."""
import functools, http.server, os, socketserver, sys

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")

class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()
    def log_message(self, *a): pass

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4173
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port),
            functools.partial(H, directory=ROOT)) as httpd:
        print(f"serving {ROOT} on http://127.0.0.1:{port}")
        httpd.serve_forever()
