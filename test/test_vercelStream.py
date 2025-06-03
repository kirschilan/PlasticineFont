import unittest
import sys
import os
#sys.path.insert(0, os.path.abspath("."))  # add the root folder to Python path

from api.render import handler
from plasticinefont.renderer import generate_text_image
from plasticinefont import config


def test_generate_text_image_to_stream():
    from io import BytesIO
    from plasticinefont.renderer import generate_text_image

    buffer = BytesIO()
    generate_text_image("HI", output_stream=buffer)
    buffer.seek(0)
    content = buffer.read()

    assert content[:8] == b'\x89PNG\r\n\x1a\n', "Output is not a valid PNG"
    assert len(content) > 100, "PNG content too short, something went wrong"

def test_handler_returns_png():
    from types import SimpleNamespace

    # Simulate Vercel-style request and response objects
    request = SimpleNamespace(args={"text": "TEST"})
    response = SimpleNamespace(status_code=None, headers={}, body=None)

    response = handler(request, response)

    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "image/png"
    assert response.body[:8] == b'\x89PNG\r\n\x1a\n'


def test_generate_text_image_skips_unsupported_chars():
    from io import BytesIO

    buffer = BytesIO()
    generate_text_image("HI@", output_stream=buffer)  # Assuming @ doesn't exist
    buffer.seek(0)
    assert buffer.read()[:8] == b'\x89PNG\r\n\x1a\n'

def test_generate_text_image_to_file_regression(tmp_path):
    output_file = tmp_path / "output.png"
    generate_text_image("HI", output_path=str(output_file))

    assert output_file.exists()
    assert output_file.read_bytes()[:8] == b'\x89PNG\r\n\x1a\n'

def test_glyphs_accessible_from_vercel():
    folder = config.DEFAULT_LETTER_FOLDER
    print("Checking glyph folder:", folder)
    assert os.path.exists(folder), "Glyph folder missing"
    assert os.listdir(folder), "Glyph folder is empty"
