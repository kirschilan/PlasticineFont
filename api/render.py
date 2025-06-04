from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from plasticinefont.renderer import generate_text_image
from io import BytesIO

def render_image(text, spacing):
    output = BytesIO()
    generate_text_image(
        text=text,
        output_stream=output,
        spacing=spacing
    )
    output.seek(0)
    return output.read()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        text = query.get("text", ["WAY TO GO"])[0]
        spacing = int(query.get("spacing", [10])[0])
        image_bytes = render_image(text, spacing)
        self.send_response(200)
        self.send_header("Content-type", "image/png")
        self.end_headers()
        self.wfile.write(image_bytes)