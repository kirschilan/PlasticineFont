from config import DEFAULT_LETTER_FOLDER
from plasticinefont.renderer import generate_text_image
from io import BytesIO
from PIL import Image
import os

def handler(request, response):
    text = request.args.get("text", "WAY TO GO")
    letter_folder = request.args.get("letter_folder", DEFAULT_LETTER_FOLDER)
    spacing = int(request.args.get("spacing", 10))

    output = BytesIO()
    generate_text_image(
        text=text,
        output_path=None,  # Explicitly prevent accidental use
        output_stream=output,
        letter_folder=letter_folder,
        spacing=spacing
    )

    output.seek(0)
    response.status_code = 200
    response.headers["Content-Type"] = "image/png"
    response.body = output.read()
    return response
