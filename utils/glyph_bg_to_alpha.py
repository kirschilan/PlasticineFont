from rembg import remove
from PIL import Image

input_path = "output/glyphs_sdxl/A.png"
output_path = "output/glyphs_sdxl/A_transparent.png"

input_image = Image.open(input_path)
output_image = remove(input_image)
output_image.save(output_path)
