import os
from PIL import Image
from plasticinefont.glyph.crop import tight_crop

from PIL import Image

import os
from PIL import Image

def load_and_process_glyph(char, letter_folder, glyph_target_height, canvas_height):
    glyph_path = os.path.join(letter_folder, f"{char}.png")
    if not os.path.exists(glyph_path):
        return None
    glyph = Image.open(glyph_path).convert("RGBA")

    # Tight crop to non-transparent content (no margin)
    bbox = glyph.getbbox()
    if bbox:
        glyph = glyph.crop(bbox)

    # Always resize to exact target height
    w, h = glyph.size
    scale = glyph_target_height / h
    new_w = int(round(w * scale))
    glyph = glyph.resize((new_w, glyph_target_height), Image.LANCZOS)

    # Paste onto a blank canvas, vertically centered
    canvas = Image.new("RGBA", (new_w, canvas_height), (255, 255, 255, 0))
    y_offset = (canvas_height - glyph_target_height) // 2
    canvas.paste(glyph, (0, y_offset), glyph)
    return canvas
'''def load_and_process_glyph(char, folder, glyph_target_height, canvas_height):
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
'''