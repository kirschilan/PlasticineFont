# 🧱 PlasticineFont

PlasticineFont is a Python tool that generates images of text using handcrafted, plasticine-style letters. It's ideal for creating playful and tactile typographic designs.
![Sample Output](output/sample_output.png)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- **Custom Letter Tiles**: Generate images using uppercase English letters crafted from  plasticine clay.
- **Transparent Backgrounds**: Outputs PNG images with transparent backgrounds for seamless integration.
# - **Configurable Spacing**: Adjust spacing between letters and words to suit your design needs.
- **Extensible Design**: Structured to support additional character sets, including lowercase letters, Hebrew characters, and special symbols.

---

## 🗂️ Project Structure
PlasticineFont/
├── data/
|     AlphaCaps
│     └── AlphaCaps/ # PNG images for A-Z uppercase letters
├── output/ # Generated output images
├── test/
│   └── Tests folder
├── test/
│   └── python source files folder
├── .gitignore # Specifies files to ignore in version control
└── README.md # Project documentation


---

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher
- [Pillow](https://python-pillow.org/) library for image processing

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kirschilan/PlasticineFont.git
   cd PlasticineFont

2. Install Dependencies
   pip install -r requirements.txt

# Usage (WIP)
  python String2PNG.py "HELLO WORLD"

By default, the script will:
Use images from ./data/AlphaCaps/
Save the output to ./output/output.png
Apply default spacing settings

# Customization
You can modify the following parameters in the script:
letter_folder: Path to the directory containing letter images.
output_path: Destination path for the generated image.
spacing: Space between letters.
space_width: Width of the space character.

✅ Testing
Ensure the functionality of the script by running the provided unit tests:
  pytest

📌 Roadmap
 • ✅ Generate images from uppercase English letters
 • Improve uppercase letterset
 • Fix space char bugs
 • Package as a Python module for easier integration
 • Add UI
 • Add colorizing 
 • Add font size
 • Add support for lowercase letters
 • Incorporate Hebrew characters
 • Include special symbols and punctuation
 • Develop a GUI for user-friendly interaction
 
🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

📄 License
## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


📬 Contact
For questions or suggestions, please open an issue on the GitHub repository.

