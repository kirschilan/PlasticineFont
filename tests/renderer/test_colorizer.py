from PIL import Image, ImageStat
import os
from io import BytesIO
from plasticinefont.glyph import colorizer, loader


def test_colorize_image_returns_image():
    image = Image.new("RGBA", (100, 100), (255, 255, 255, 255))
    result = colorizer.colorize_image(image, (238, 174, 104))
    assert isinstance(result, Image.Image)  # will fail unless we return something

def test_colorize_image_changes_color():
    char = "A"
    folder = os.path.join("data", "AlphaCaps")
    glyph_target_height = 100
    canvas_height = 100
    requested_color = (0, 255, 0)  # green

    original = loader.load_and_process_glyph(char, folder, glyph_target_height, canvas_height)
    recolored = colorizer.colorize_image(original, requested_color)

    # Convert image to byte stream, reload for pixel inspection
    img_bytes = BytesIO()
    recolored.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    img = Image.open(img_bytes).convert("RGBA")

    pixels = img.getdata()
    color_found = any(pixel[:3] == requested_color for pixel in pixels)

    # This will fail — colorizer doesn't change color yet
    assert color_found, "Recolored glyph does not contain the requested color"
