from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from plasticinefont.renderer import generate_text_image
from io import BytesIO

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        query = parse_qs(urlparse(self.path).query)
        text = query.get("text", ["WAY TO GO"])[0]
        spacing = int(query.get("spacing", [10])[0])

        # Generate image
        output = BytesIO()
        generate_text_image(
            text=text,
            output_stream=output,
            spacing=spacing
        )
        output.seek(0)
        image_bytes = output.read()

        # Send response
        self.send_response(200)
        self.send_header('Content-type','image/png')
        self.end_headers()
        self.wfile.write(image_bytes)
