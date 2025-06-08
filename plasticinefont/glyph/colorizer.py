from PIL import Image
import numpy as np

def colorize_image(image: Image.Image, target_rgb: tuple[int, int, int]) -> Image.Image:
    """
    Apply a soft color tint to a transparent plasticine glyph image.

    Args:
        image (PIL.Image.Image): The input RGBA glyph image.
        target_rgb (tuple[int, int, int]): The (R, G, B) color to tint the glyph.

    Returns:
        PIL.Image.Image: The colorized image, preserving texture and transparency.

    Raises:
        ValueError: If the input image is None or not in RGBA mode.
    """
    if image is None:
        raise ValueError("Input image is None. Check that the glyph file exists and is loaded correctly.")
    
    if image.mode != "RGBA":
        raise ValueError("Input image must be in RGBA mode")

    # Convert image to normalized float32 numpy array
    base_np = np.array(image).astype(np.float32) / 255.0

    # Prepare tint layer
    tint_np = np.ones_like(base_np)
    tint_np[..., 0] *= target_rgb[0] / 255.0
    tint_np[..., 1] *= target_rgb[1] / 255.0
    tint_np[..., 2] *= target_rgb[2] / 255.0
    tint_np[..., 3] = base_np[..., 3]  # preserve alpha

    # Multiply RGB channels
    blended_rgb = base_np[..., :3] * tint_np[..., :3]

    # Combine RGB with original alpha
    result_np = np.dstack((blended_rgb, base_np[..., 3]))

    # Convert back to PIL image
    result_img = Image.fromarray((result_np * 255).astype(np.uint8), mode="RGBA")
    return result_img