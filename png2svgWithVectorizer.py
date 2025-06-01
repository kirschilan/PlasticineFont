from vectorizer import Vectorizer

# Initialize
v = Vectorizer()

# Input/output
input_png = "input/a.png"
output_svg = "svg/a.svg"

# Convert and save
v.convert_image(input_png, output_svg)

print(f"✅ Saved SVG to {output_svg}")
