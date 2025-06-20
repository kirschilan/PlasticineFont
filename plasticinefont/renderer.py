# Re-imports after kernel reset
import os
from io import BytesIO
from PIL import Image, ImageOps
from plasticinefont.config import DEFAULT_LETTER_FOLDER
from plasticinefont.glyph.loader import load_and_process_glyph
from plasticinefont.glyph.colorizer import colorize_image



def generate_text_image(
    text,
    output_path=None,
    output_stream=None,
    letter_folder=DEFAULT_LETTER_FOLDER,
    spacing=10,
    space_width=40,
    glyph_target_height=256,
    canvas_height=280,
    color=None  # <- NEW: should be a tuple like (238, 174, 104)
):
    """
    Render a string as an image using plasticine glyphs, with optional colorization.

    Args:
        text (str): The text to render.
        output_path (str, optional): Path to save the output PNG.
        output_stream (file-like, optional): Stream to write the PNG to.
        letter_folder (str): Path to glyph images.
        spacing (int): Space between letters (pixels).
        space_width (int): Width of space character (pixels).
        glyph_target_height (int): Height to scale each glyph to (pixels).
        canvas_height (int): Height of the output image (pixels).
        color (tuple[int, int, int], optional): RGB color for tinting glyphs.

    Returns:
        bytes: The PNG image as bytes if no output_path or output_stream is given.

    Raises:
        FileNotFoundError: If no valid letter images are found for the input text.
    """
    letter_images = []

    for char in text.upper():
        if char == " ":
            space_img = Image.new("RGBA", (space_width, canvas_height), (255, 255, 255, 0))
            letter_images.append(space_img)
            continue
        glyph = load_and_process_glyph(char, letter_folder, glyph_target_height, canvas_height)
        if glyph is not None:
            if color:
                glyph = colorize_image(glyph, color)
            if glyph:
                letter_images.append(glyph)

    if not letter_images:
        raise FileNotFoundError(
            f"No valid letter images found for input '{text}'. "
            f"Check if all characters have corresponding image files in '{letter_folder}'."
        )
    
    total_width = sum(im.width for im in letter_images) + spacing * (len(letter_images) - 1)
    output_img = Image.new("RGBA", (total_width, canvas_height), (255, 255, 255, 0))

    x_offset = 0
    for im in letter_images:
        output_img.paste(im, (x_offset, 0), im)
        x_offset += im.width + spacing

    if output_stream is not None:
        output_img.save(output_stream, format="PNG")
    elif output_path is not None:
        output_dir = os.path.dirname(output_path) or "."
        os.makedirs(output_dir, exist_ok=True)
        output_img.save(output_path)
        print(f"✅ Image saved to {output_path}")
    else:
        raise ValueError("Either output_path or output_stream must be provided.")

# Example usage:
if __name__ == "__main__":
    generate_text_image("WAY TO GO")  # Only A-Z supported, will ignore non-letters