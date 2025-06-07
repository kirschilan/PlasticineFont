import os
from unittest.mock import MagicMock

from utils.generate_glyphs import fetch_and_save_glyphs

def test_fetch_and_save_glyphs(tmp_path):
    letters = "AB"
    prompt_template = "Letter: {letter}"
    output_dir = tmp_path / "glyphs"
    fake_url = "http://fake.url/image.png"
    fake_image = b"fakeimage"

    # Mock OpenAI image create
    def mock_openai_image_create(**kwargs):
        assert "prompt" in kwargs
        return {'data': [{'url': fake_url}]}

    # Mock image downloader
    def mock_image_downloader(url):
        assert url == fake_url
        return fake_image

    fetch_and_save_glyphs(
        letters,
        prompt_template,
        str(output_dir),
        mock_openai_image_create,
        mock_image_downloader,
    )

    # Assert files were created
    for letter in letters:
        path = output_dir / f"{letter}.png"
        assert path.exists()
        assert path.read_bytes() == fake_image

def test_capital_alpha_saved_to_alphacaps(tmp_path):
    letters = "A"
    prompt_template = "Letter: {letter}"
    output_dir = tmp_path / "output"
    fake_url = "http://fake.url/image.png"
    fake_image = b"fakeimage"

    def mock_openai_image_create(**kwargs):
        return {'data': [{'url': fake_url}]}

    def mock_image_downloader(url):
        return fake_image

def test_fetch_and_save_glyphs(tmp_path):
    letters = "A"
    prompt_template = "Letter: {letter}"
    output_dir = tmp_path / "glyphs"
    fake_url = "http://fake.url/image.png"
    fake_image = b"fakeimage"

    def mock_openai_image_create(**kwargs):
        return {'data': [{'url': fake_url}]}

    def mock_image_downloader(url):
        return fake_image

    from utils.generate_glyphs import fetch_and_save_glyphs
    fetch_and_save_glyphs(
        letters,
        prompt_template,
        str(output_dir),
        mock_openai_image_create,
        mock_image_downloader,
    )

    # Assert file is in AlphaCaps subfolder
    path = output_dir / "AlphaCaps" / f"{letters[0]}.png"
    assert path.exists()
    assert path.read_bytes() == fake_image
    glyph_path = output_dir / "AlphaCaps" / "A.png"
    assert glyph_path.exists(), "Capital A should be saved to AlphaCaps folder"
    assert glyph_path.read_bytes() == fake_image