import os

def fetch_and_save_glyphs(
    letters,
    prompt_template,
    output_dir,
    openai_image_create,
    image_downloader,
):
    os.makedirs(output_dir, exist_ok=True)
    for letter in letters:
        prompt = prompt_template.format(letter=letter)
        response = openai_image_create(
            prompt=prompt,
            n=1,
            size="512x512",
            response_format="url"
        )
        image_url = response['data'][0]['url']
        image_path = os.path.join(output_dir, f"{letter}.png")
        img_data = image_downloader(image_url)
        with open(image_path, "wb") as f:
            f.write(img_data)

if __name__ == "__main__":
    from openai import OpenAI
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    import requests

    template_prompt = (
        "Generate a plasticine-style capital letter '{letter}'. "
        "Match the style of this example: light off-white plasticine, soft shadow, clean background, "
        "centered letter, same lighting, and same resolution. Output only the image."
    )
#    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letters = "AB"
    output_dir = "output/glyphs_interim"

    def openai_image_create(**kwargs):
        return client.images.generate(**kwargs)

    def image_downloader(url):
        return requests.get(url).content

    fetch_and_save_glyphs(
        letters,
        template_prompt,
        output_dir,
        openai_image_create,
        image_downloader,
    )