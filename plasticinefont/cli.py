import os
from plasticinefont.config import DEFAULT_LETTER_FOLDER
from .renderer import generate_text_image
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("--output", required=True)
    parser.add_argument("--letter-folder", default=DEFAULT_LETTER_FOLDER)
    args = parser.parse_args()

    # Normalize path if relative
    letter_folder = os.path.abspath(args.letter_folder)

    generate_text_image(
        text=args.text,
        output_path=args.output,
        letter_folder=letter_folder
    )
