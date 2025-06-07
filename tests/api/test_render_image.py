from api.render import render_image

def test_render_image_creates_png():
    img_bytes = render_image("TEST", 10)
    assert img_bytes[:8] == b'\x89PNG\r\n\x1a\n'  # PNG file signature
    assert len(img_bytes) > 100  # Should be a non-trivial image

def test_render_image_accepts_color_but_does_not_use_it():
    color = (238, 174, 104)
    
    render_image("A", spacing=10, color=color)
