import unittest
import sys
import os
from PIL import Image
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.String2PNG import generate_text_image

def project_path(*subdirs):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", *subdirs))

class TestGenerateTextImage(unittest.TestCase):

    def setUp(self):
        self.letter_folder = project_path("data", "AlphaCaps")
        self.output_file = project_path("output", "test_output.png")
        if not os.path.isdir(self.letter_folder):
            self.skipTest("AlphaCaps folder not found")

    def tearDown(self):
        if os.path.isfile(self.output_file):
            os.remove(self.output_file)

    def test_simple_word(self):
        generate_text_image("HELLO", output_path=self.output_file, letter_folder=self.letter_folder)
        self.assertTrue(os.path.exists(self.output_file))
        img = Image.open(self.output_file)
        self.assertGreater(img.width, 0)
        self.assertGreater(img.height, 0)

    def test_space_handling(self):
        generate_text_image("WAY TO GO", output_path=self.output_file, letter_folder=self.letter_folder)
        self.assertTrue(os.path.exists(self.output_file))
        img = Image.open(self.output_file)
        self.assertGreater(img.width, 0)

    def test_ignores_lowercase(self):
        generate_text_image("hello", output_path=self.output_file, letter_folder=self.letter_folder)
        self.assertTrue(os.path.exists(self.output_file))
        img = Image.open(self.output_file)
        self.assertGreater(img.width, 0)

    def test_ignores_invalid_chars(self):
        generate_text_image("HELLO!", output_path=self.output_file, letter_folder=self.letter_folder)
        self.assertTrue(os.path.exists(self.output_file))
        img = Image.open(self.output_file)
        self.assertGreater(img.width, 0)

    def test_empty_input_raises(self):
        with self.assertRaises(ValueError):
            generate_text_image("123456", output_path=self.output_file, letter_folder=self.letter_folder)

    def test_missing_letter_raises(self):
        missing_path = os.path.join(self.letter_folder, "Z.png")
        if os.path.exists(missing_path):
            os.rename(missing_path, missing_path + ".bak")
        try:
            with self.assertRaises(FileNotFoundError):
                generate_text_image("Z", output_path=self.output_file, letter_folder=self.letter_folder)
        finally:
            if os.path.exists(missing_path + ".bak"):
                os.rename(missing_path + ".bak", missing_path)

if __name__ == "__main__":
    unittest.main()
