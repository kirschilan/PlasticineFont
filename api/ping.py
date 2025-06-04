from http.server import BaseHTTPRequestHandler

def get_pong():
    return "pong"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        pong = get_pong()
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(pong.encode())