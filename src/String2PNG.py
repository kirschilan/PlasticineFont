# Re-imports after kernel reset
import os
from PIL import Image, ImageOps

def tight_crop(image, margin=2, min_alpha=5):
    """Crop the image to the visible glyph area with some margin."""
    alpha = image.split()[-1]
    bw = alpha.point(lambda a: 255 if a > min_alpha else 0)
    bbox = bw.getbbox()
    if not bbox:
        return image
    left = max(bbox[0] - margin, 0)
    top = max(bbox[1] - margin, 0)
    right = min(bbox[2] + margin, image.width)
    bottom = min(bbox[3] + margin, image.height)
    return image.crop((left, top, right, bottom))

def generate_text_image(
    text,
    output_path="./output/output.png",
    letter_folder="./data/AlphaCaps",
    spacing=10,
    space_width=40,
    glyph_target_height=80,
    canvas_height=100
):
    letter_images = []

    for char in text.upper():
        if char == " ":
            space_img = Image.new("RGBA", (space_width, canvas_height), (255, 255, 255, 0))
            letter_images.append(space_img)
            continue

        letter_path = os.path.join(letter_folder, f"{char}.png")
        if not os.path.exists(letter_path):
            continue  # skip unsupported characters

        img = Image.open(letter_path).convert("RGBA")

        # Tightly crop visible content with margin
        img = tight_crop(img, margin=2)

        # Resize glyph content to consistent height
        if img.height != glyph_target_height:
            new_width = int((glyph_target_height / img.height) * img.width)
            img = img.resize((new_width, glyph_target_height), Image.LANCZOS)

        # Paste onto standard canvas
        canvas = Image.new("RGBA", (img.width, canvas_height), (255, 255, 255, 0))
        y_offset = (canvas_height - glyph_target_height) // 2
        canvas.paste(img, (0, y_offset), img)

        letter_images.append(canvas)

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

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output_img.save(output_path)
    print(f"✅ Image saved to {output_path}")

# Example usage:
if __name__ == "__main__":
    generate_text_image("WAY TO GO")  # Only A-Z supported, will ignore non-letters