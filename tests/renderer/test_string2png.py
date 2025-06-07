import unittest
from unittest.mock import patch, ANY
import sys
import os
import tempfile
from PIL import Image
from io import BytesIO


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from plasticinefont.renderer import generate_text_image

def project_path(*subdirs):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", *subdirs))

class TestGenerateTextImage(unittest.TestCase):

    def setUp(self):
        self.letter_folder = project_path("data", "AlphaCaps")
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_file = os.path.join(self.temp_dir.name, "test_output.png")
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
        with self.assertRaises(FileNotFoundError):
            generate_text_image("123456", output_path=self.output_file, letter_folder=self.letter_folder)


    def test_fails_on_missing_letter_file(self):
        test_string = "Ñ"  # Not supported by current glyph set
        with self.assertRaises(FileNotFoundError):
            generate_text_image(test_string, output_path=self.output_file, letter_folder=self.letter_folder)

    def test_missing_glyph_raises_with_message(self):
        test_string = "Ñ"
        with self.assertRaises(FileNotFoundError) as context:
            generate_text_image(test_string, output_path=self.output_file, letter_folder=self.letter_folder)

        msg = str(context.exception)
        self.assertIn("No valid letter images found", msg)
        self.assertIn(test_string, msg)
        self.assertIn(self.letter_folder, msg)

    def test_render_glyph_invokes_colorizer_with_color(self):
        dummy_image = Image.new("RGBA", (100, 100), (255, 255, 255, 255))
        dummy_output = BytesIO()

        with patch("plasticinefont.renderer.colorize_image", return_value=dummy_image) as mock_colorize, \
            patch("plasticinefont.glyph.loader.load_and_process_glyph", return_value=dummy_image):
            
            generate_text_image("A", output_stream=dummy_output, color=(238, 174, 104))
            
            mock_colorize.assert_called_once_with(ANY, (238, 174, 104))


if __name__ == "__main__":
    unittest.main()
