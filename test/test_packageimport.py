import unittest
import pytest
import sys
import os
import subprocess

def test_import_string2png_module():
    try:
        from plasticinefont.renderer import generate_text_image
    except ImportError:
        pytest.fail("Failed to import generate_text_image from plasticinefont.string2png")


def test_cli_invocation():
    result = subprocess.run(
        ["string2png", "HI", "--output", "test_output.png"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    assert "Image saved" in result.stdout

def test_installed_package_generates_image(tmp_path):
    from plasticinefont.renderer import generate_text_image
    output_path = tmp_path / "out.png"
    generate_text_image("YES", output_path=str(output_path))

    assert output_path.exists(), "Output PNG was not created"
    assert output_path.stat().st_size > 100, "Generated PNG seems empty"

def test_letter_folder_accessibility():
    from plasticinefont import renderer
    assert os.path.exists(renderer.DEFAULT_LETTER_FOLDER), f"Missing glyphs folder: {renderer.DEFAULT_LETTER_FOLDER}"

if __name__ == "__main__":
    unittest.main()
