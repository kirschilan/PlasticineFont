import os
from PIL import Image
from plasticinefont.glyph.crop import tight_crop


def load_and_process_glyph(char, folder, glyph_target_height, canvas_height):
    letter_path = os.path.join(folder, f"{char}.png")
    if not os.path.exists(letter_path):
        return None

    img = Image.open(letter_path).convert("RGBA")
    img = tight_crop(img, margin=2)

    if img.height != glyph_target_height:
        new_width = int((glyph_target_height / img.height) * img.width)
        img = img.resize((new_width, glyph_target_height), Image.LANCZOS)

    canvas = Image.new("RGBA", (img.width, canvas_height), (255, 255, 255, 0))
    y_offset = (canvas_height - glyph_target_height) // 2
    canvas.paste(img, (0, y_offset), img)
    return canvas