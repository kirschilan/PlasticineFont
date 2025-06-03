from .renderer import generate_text_image
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("--output", required=True)
    parser.add_argument("--letter-folder", default="data/AlphaCaps")
    args = parser.parse_args()
    generate_text_image(args.text, args.output, args.letter_folder)
