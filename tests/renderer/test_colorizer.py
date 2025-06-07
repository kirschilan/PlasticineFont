from PIL import Image
from plasticinefont.glyph import colorizer

def test_colorize_image_returns_image():
    image = Image.new("RGBA", (100, 100), (255, 255, 255, 255))
    result = colorizer.colorize_image(image, (238, 174, 104))
    assert isinstance(result, Image.Image)  # will fail unless we return something
