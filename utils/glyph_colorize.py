from PIL import Image
import numpy as np
import sys

def colorize_plasticine(input_path, output_path, target_rgb):
    base = Image.open(input_path).convert("RGBA")
    
    # Split channels
    r, g, b, a = base.split()

    # Convert to numpy for blending
    base_np = np.array(base).astype(np.float32) / 255.0
    tint_np = np.ones_like(base_np)
    tint_np[..., 0] *= target_rgb[0] / 255.0
    tint_np[..., 1] *= target_rgb[1] / 255.0
    tint_np[..., 2] *= target_rgb[2] / 255.0
    tint_np[..., 3] = base_np[..., 3]  # preserve original alpha

    # Multiply (blending the color)
    blended_np = base_np[..., :3] * tint_np[..., :3]
    blended = np.dstack((blended_np, base_np[..., 3]))  # reattach alpha
    blended_img = Image.fromarray((blended * 255).astype(np.uint8), mode="RGBA")

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
