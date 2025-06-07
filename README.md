# 🧱 PlasticineFont

PlasticineFont is a tool that generates images of text using handcrafted, plasticine-style letters. It's ideal for creating playful and tactile typographic designs.

![Sample Output](output/sample_output.png)

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Customization](#customization)
- [Colorizing Glyphs](#colorizing-glyphs)
- [Testing](#testing)
- [Dependencies](#dependencies)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## ✨ Features

- **Custom Letter Tiles**: Generate images using uppercase characters crafted from plasticine clay.
- **Transparent Backgrounds**: Outputs PNG images with transparent backgrounds for seamless integration.
- **Configurable Spacing**: Adjust spacing between letters and words to suit your design needs.
- **Colorization**: Tint glyphs with any RGB color while preserving texture and transparency.
- **Extensible Design**: Structured to support additional character sets, including lowercase letters, Hebrew characters, and special symbols.

---

## 🗂️ Project Structure

```
PlasticineFont/
├── data/
│   └── AlphaCaps/         # PNG images for A-Z uppercase letters
                           # (additional characters in future releases) 
├── output/                # Generated output images
├── tests/                 # Unit and integration tests
├── plasticinefont/
│   └── glyph/
│       └── colorizer.py   # Colorization logic
├── utils/                 # utilities for generating glyphs. depends on ClayMate from CivitAI (requires registration and download, per SDXL instructions)
├── .gitignore             # Specifies files to ignore in version control
└── README.md              # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- [Pillow](https://python-pillow.org/) for image processing
- [numpy](https://numpy.org/) for colorization
- [openai](https://pypi.org/project/openai/) for glyph generation (optional, for utils)
- [requests](https://pypi.org/project/requests/) for downloading images (optional, for utils)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kirschilan/PlasticineFont.git
   cd PlasticineFont
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

---

## 🖥️ Usage

To generate a PNG from a string:
```bash
python String2PNG.py "HELLO WORLD"
```

By default, the script will:
- Use images from `./data/AlphaCaps/`
- Save the output to `./output/output.png`
- Apply default spacing settings

---

## ⚙️ Customization

You can modify the following parameters in the script:
- `letter_folder`: Path to the directory containing letter images.
- `output_path`: Destination path for the generated image.
- `spacing`: Space between letters.
- `space_width`: Width of the space character.

---

## 🎨 Colorizing Glyphs

You can colorize a glyph image using the `colorize_image` function:

```python
from PIL import Image
from plasticinefont.glyph.colorizer import colorize_image

img = Image.open("data/AlphaCaps/A.png")
colored = colorize_image(img, (238, 174, 104))  # Example RGB color
colored.save("output/colored_A.png")
```

---

## ✅ Testing

Run all tests with:
```bash
pytest
```

---

## 📦 Dependencies

- Pillow
- numpy
- openai (for glyph generation)
- requests (for downloading images)
- pytest (for testing)
- pygments, olefile, fs (as needed for your utils)

---

## 📌 Roadmap

- ✅ Generate images from uppercase English letters
- ✅ Add colorizing feature
- Improve uppercase letterset
- Add UI
- Add font size
- Add support for lowercase letters
- Incorporate Hebrew characters
- Include special symbols and punctuation
- Develop a GUI for user-friendly interaction

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

For questions or suggestions, please open an issue on the GitHub repository.

