from diffusers import StableDiffusionXLPipeline
import torch
from PIL import Image
import numpy as np

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",  # Or another SDXL model
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True,
    safety_checker=None  # Optional
).to("cuda")

"""
prompt = (
    "a single centered full-body sprite of a palm tree, realistic and FSR"
    "standing upright, isolated, no background, no shadow, no ground, facing forward clearn anatomy"
)
"""

prompt = (
    "a single, front-facing, full colored portrait of an adventurer, arms extended horizontally, wearing leather clothes, realistic style, isolated, no shadows, no ground, no extra figures, clear anatomy, centered, high detail"
    )

negative_prompt = (
    "multiple characters, multiple viewpoints, duplicates, side view, back view, blurred, cropped, watermark, shadow, ground, background, group, extra limbs, overlay, out of frame"
    )

image = pipe(prompt=prompt, negative_prompt=negative_prompt).images[0]

# Optional: convert white background to transparent

image.save("sprite/sd_output.jpg")  # Save as PNG for transparency
