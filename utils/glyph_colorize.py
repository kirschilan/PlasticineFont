from PIL import Image
from plasticinefont.glyph import colorizer
import sys

def colorize_plasticine(input_path, output_path, target_rgb):
    base = Image.open(input_path).convert("RGBA")
    
    blended_img = colorizer.colorize_image(base, target_rgb)
    if blended_img is None:
        print("Error: Colorization failed.")
        return
    blended_img.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python colorize_glyph.py <input.png> <output.png> <R> <G> <B>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    r = int(sys.argv[3])
    g = int(sys.argv[4])
    b = int(sys.argv[5])
    
    colorize_plasticine(input_file, output_file, (r, g, b))
