import os
from PIL import Image

def generate_text_image(
    text,
    output_path="./output/output.png",
    letter_folder="./data/AlphaCaps",
    spacing=10,
    space_width=40
):
    text = text.upper()
    valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    text = ''.join([c for c in text if c in valid_chars])

    if not text:
        raise ValueError("Input must contain at least one valid capital letter (A–Z or space).")

    # Step 1: Preload letters (except spaces) to determine max height
    preloaded = {}
    max_height = 0
    for char in set(text):
        if char == " ":
            continue
        filepath = os.path.join(letter_folder, f"{char}.png")
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Missing image for letter '{char}' at {filepath}")
        img = Image.open(filepath).convert("RGBA")
        preloaded[char] = img
        max_height = max(max_height, img.height)

    # Step 2: Build letter list
    letters = []
    for char in text:
        if char == " ":
            space_img = Image.new("RGBA", (space_width, max_height), (0, 0, 0, 0))
            letters.append(space_img)
        else:
            letters.append(preloaded[char])

    # Step 3: Combine into one image
    total_width = sum(img.width for img in letters) + spacing * (len(letters) - 1)
    output_image = Image.new("RGBA", (total_width, max_height), (0, 0, 0, 0))

    x = 0
    for img in letters:
        output_image.paste(img, (x, (max_height - img.height) // 2), img)
        x += img.width + spacing

    output_image.save(output_path)
    print(f"✅ Image saved to {output_path}")

# Example usage:
if __name__ == "__main__":
    generate_text_image("WAY TO GO")  # Only A-Z supported, will ignore non-letters
