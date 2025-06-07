import os
from openai import OpenAI, BadRequestError
import requests

def get_glyph_subfolder(letter):
    if letter.isupper() and letter.isalpha() and letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return "AlphaCaps"
    # Add more rules for other scripts/char types here
    return "Other"

def fetch_and_save_glyphs(
    letters,
    prompt_template,
    output_dir,
    openai_image_create,
    image_downloader,
):
    for letter in letters:
        subfolder = get_glyph_subfolder(letter)
        letter_dir = os.path.join(output_dir, subfolder)
        os.makedirs(letter_dir, exist_ok=True)
        prompt = prompt_template.format(letter=letter)
        response = openai_image_create(
            prompt=prompt,
            n=1
            #size="512x512",
            #response_format="url"
        )
        image_url = response['data'][0]['url']
        image_path = os.path.join(letter_dir, f"{letter}.png")
        img_data = image_downloader(image_url)
        with open(image_path, "wb") as f:
            f.write(img_data)

if __name__ == "__main__":
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    template_prompt = (
        "A clay sculpture of the capital letter '{letter}' on a plain background. Off-white material, soft shadow, centered."
        #"A plasticine capital letter '{letter}', centered on a clean background. Light off-white clay, soft shadow, consistent lighting. Minimalist and neat."
        #'''"Generate a plasticine-style capital letter '{letter}'. "
        #"Match the style of this example: light off-white plasticine, soft shadow, clean background, "
        #"centered letter, same lighting, and same resolution. Output only the image."'''
    )


#    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letters = "AB"
    output_dir = "output/glyphs_interim"

    def openai_image_create(**kwargs):
        prompt = kwargs.get("prompt")
        print(f"Prompt: {prompt}")
        try:
            return client.images.generate(
                model="dall-e-2",
                prompt=prompt,
                size="512x512",            # 1024x1024 also valid
                response_format="url",     # Optional, default is "url"
                n=1                        # Required for dall-e-2
            )
        except OpenAI.BadRequestError as e:
            print("API rejected request:")
            print(e.response)
            raise

    
    def image_downloader(url):
        return requests.get(url).content

    fetch_and_save_glyphs(
        letters,
        template_prompt,
        output_dir,
        openai_image_create,
        image_downloader,
    )