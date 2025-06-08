import unittest
import sys
import os
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from plasticinefont.renderer import generate_text_image

'''
def estimate_letter_height_by_mass(alpha, x_start, x_end, min_mass_per_row=3):
    height = alpha.height
    visible_rows = 0
    for y in range(height):
        row_mass = sum(
            1 for x in range(x_start, x_end) if alpha.getpixel((x, y)) > 0
        )
        if row_mass >= min_mass_per_row:
            visible_rows += 1
    return visible_rows
'''

def get_letter_height_from_alpha(alpha, x_start, x_end):
    top = None
    bottom = None
    for y in range(alpha.height):
        for x in range(x_start, x_end):
            if alpha.getpixel((x, y)) > 0:
                if top is None:
                    top = y
                bottom = y
    if top is None or bottom is None:
        return 0
    return bottom - top + 1


def detect_letter_bounds(alpha, width, height, min_gap=4, min_width=10):
    """Yields (x_start, x_end) of detected letter regions."""
    in_letter = False
    x_start = None
    space_counter = 0

    for x in range(width):
        column = [alpha.getpixel((x, y)) for y in range(height)]
        has_content = any(px > 0 for px in column)

        if has_content:
            if not in_letter:
                in_letter = True
                x_start = x
            space_counter = 0
        else:
            if in_letter:
                space_counter += 1
                if space_counter > min_gap:
                    x_end = x - space_counter
                    if x_end - x_start > min_width:
                        yield (x_start, x_end)
                    in_letter = False
                    space_counter = 0

    if in_letter and x_start is not None:
        x_end = width
        if x_end - x_start > min_width:
            yield (x_start, x_end)

class TestLetterRendering(unittest.TestCase):
    def test_rendered_letters_have_consistent_height(self):
        test_string = "WAYTOGO"
        output_path = "./output/test_uniform_height.png"
        generate_text_image(test_string, output_path=output_path)

        img = Image.open(output_path).convert("RGBA")
        alpha = img.split()[-1]
        width, height = img.size

        letter_heights = [
            get_letter_height_from_alpha(alpha, x_start, x_end)
            for x_start, x_end in detect_letter_bounds(alpha, width, height)
        ]

        if len(letter_heights) != len(test_string):
            print(f"⚠️ Expected {len(test_string)} letters but found {len(letter_heights)}: {letter_heights}")
            img.save("./output/debug_letters.png")

        self.assertEqual(len(letter_heights), len(test_string))

        max_height = max(letter_heights)
        min_height = min(letter_heights)
        tolerance_pct = 0.04  # 3%
        tolerance = int(max_height * tolerance_pct)

        self.assertLessEqual(
            max_height - min_height,
            tolerance,
            f"Height mismatch: {letter_heights}"
        )


if __name__ == "__main__":
    unittest.main()
