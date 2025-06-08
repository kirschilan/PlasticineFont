from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from plasticinefont.renderer import generate_text_image
from io import BytesIO

def render_image(text, spacing, color=None):
    output = BytesIO()
    generate_text_image(
        text=text,
        output_stream=output,
        spacing=spacing,
        color=color
    )
    output.seek(0)
    return output.read()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        text = query.get("text", ["WAY TO GO"])[0]
        spacing = int(query.get("spacing", [10])[0])

        # Extract and validate color string, with error handling
        color_str = query.get("color", [None])[0]
        color = None
        if color_str:
            try:
                color = tuple(map(int, color_str.split(",")))
                if len(color) != 3 or not all(0 <= c <= 255 for c in color):
                    raise ValueError("Color must be three integers between 0 and 255")
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(f'{{"error": "Invalid color parameter: {e}"}}'.encode())
                return

        try:
            image_bytes = render_image(text, spacing, color=color)
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            self.wfile.write(image_bytes)
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(f'{{"error": "Render failed: {e}"}}'.encode())