def tight_crop(image, margin=2, min_alpha=5):
    """Crop the image to the visible glyph area with some margin."""
    alpha = image.split()[-1]
    # Convert alpha values above `min_alpha` to 255 (opaque) and others to 0 (transparent)
    bw = alpha.point(lambda alpha_value: 255 if alpha_value > min_alpha else 0)
    bbox = bw.getbbox()
    if not bbox:
        return image
    left = max(bbox[0] - margin, 0)
    top = max(bbox[1] - margin, 0)
    right = min(bbox[2] + margin, image.width)
    bottom = min(bbox[3] + margin, image.height)
    return image.crop((left, top, right, bottom))
