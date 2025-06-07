import torch
from diffusers import StableDiffusionXLPipeline, LCMScheduler
import os

def generate_letter(letter, pipe, output_dir):
    prompt = (
        #f"A plasticine sculpture of the letter '{letter}', detailed clay texture, "
        #f"on a white background, soft shadows, claymation style"
        f"A plasticine sculpture of the capital letter '{letter}', "
        "centered on a pure white background. Front-facing, clean silhouette, no props, no background elements. "
        "Soft shadows, even lighting, smooth clay texture. Balanced, symmetrical shape. "
        "Consistent off-white clay. Designed for easy background removal."
    )
    image = pipe(
        prompt=prompt,
        height=512,
        width=512,
        guidance_scale=6.0,
        num_inference_steps=15,
    ).images[0]

    image.save(os.path.join(output_dir, f"{letter}.png"))
    print(f"Saved {letter}.png")

def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"

    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float32,
        use_safetensors=True,
        variant=None,
    )
    pipe.to(device)

    # Load LoRA weights
    lora_path = "models/lora/claymate"
    pipe.load_lora_weights(lora_path)
    pipe.fuse_lora()

    #pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)

    output_dir = "output/glyphs_sdxl"
    os.makedirs(output_dir, exist_ok=True)

    # Generate just one letter for now
    generate_letter("A", pipe, output_dir)

if __name__ == "__main__":
    main()
