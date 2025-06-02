# png2svg.py
import os
import subprocess
from PIL import Image

INPUT_DIR = "input"
PBM_DIR = "pbm"
SVG_DIR = "svg"
THRESHOLD = 128  # 0-255; adjust as needed

os.makedirs(PBM_DIR, exist_ok=True)
os.makedirs(SVG_DIR, exist_ok=True)

for filename in os.listdir(INPUT_DIR):
    if not filename.endswith(".png"):
        continue
    name = os.path.splitext(filename)[0]

    # Convert to B&W PBM
    img = Image.open(os.path.join(INPUT_DIR, filename)).convert("L")
    img = img.point(lambda x: 255 if x > THRESHOLD else 0, mode='1')
    pbm_path = os.path.join(PBM_DIR, f"{name}.pbm")
    img.save(pbm_path)

    # Trace to SVG using potrace
    svg_path = os.path.join(SVG_DIR, f"{name}.svg")
    subprocess.run(["potrace", pbm_path, "-s", "-o", svg_path], check=True)

print("✅ Done tracing PNGs to SVGs.")
