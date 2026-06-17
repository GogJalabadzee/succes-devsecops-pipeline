import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# Secure, dependency-free demo app for a DevSecOps pipeline.
# No third-party libraries -> SCA has nothing to flag -> the gate always passes.


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        # Security headers — good posture, reduces DAST findings
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'self'")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, '{"status":"ok"}', "application/json")
        elif self.path == "/" or self.path.startswith("/?"):
            self._send(200,
                "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
                "<title>Secure Demo App</title></head><body>"
                "<h1>Secure Demo App</h1>"
                "<p>Hardened, dependency-free sample application used to demonstrate "
                "a passing DevSecOps security pipeline.</p>"
                "</body></html>")
        else:
            self._send(404, "<h1>404 Not Found</h1>")

    def log_message(self, *args):
        return  # keep logs quiet


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Serving on port {port}")
    server.serve_forever()
