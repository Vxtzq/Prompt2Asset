import argparse
import torch
from diffusers import (
    StableDiffusionXLControlNetPipeline,
    ControlNetModel,
    StableDiffusionXLPipeline,
)
from diffusers.utils import load_image
from PIL import Image

def main():
    parser = argparse.ArgumentParser(description="Generate sprite using SDXL with optional ControlNet OpenPose")
    parser.add_argument(
        "--prompt",
        type=str,
        default=(
            "a single, front-facing, full colored portrait of an adventurer, arms extended horizontally, "
            "wearing leather clothes, realistic style, isolated, no shadows, no ground, no extra figures, "
            "clear anatomy, centered, high detail"
        ),
        help="Text prompt for the image generation"
    )
    parser.add_argument(
        "--negative_prompt",
        type=str,
        default=(
            "multiple characters, multiple viewpoints, duplicates, side view, back view, blurred, cropped, "
            "watermark, shadow, ground, background, group, extra limbs, overlay, out of frame"
        ),
        help="Negative prompt to avoid unwanted features"
    )
    parser.add_argument(
        "--pose_image",
        type=str,
        default="character_pose.jpeg",
        help="Path to pose reference image (used only if --use_pose is specified)"
    )
    parser.add_argument(
        "--use_pose",
        action="store_true",
        help="Enable ControlNet OpenPose guidance using --pose_image"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="sprite/sd_output.jpg",
        help="Output file path for the generated image"
    )

    args = parser.parse_args()

    if args.use_pose:
        # Load preprocessed pose image (assumed already processed like OpenPose)
        pose_image = load_image(args.pose_image).resize((1024, 1024))

        # Load ControlNet model for SDXL + OpenPose
        controlnet = ControlNetModel.from_pretrained(
            "xinsir/controlnet-openpose-sdxl-1.0",
            torch_dtype=torch.float16
        )

        # Load SDXL base model with ControlNet
        pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            controlnet=controlnet,
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True,
            safety_checker=None
        ).to("cuda")

        # VRAM optimizations
        pipe.enable_attention_slicing()
        pipe.enable_vae_slicing()
        pipe.enable_model_cpu_offload()
        try:
            pipe.enable_xformers_memory_efficient_attention()
        except Exception as e:
            print(f"⚠️ Warning: xformers attention not enabled: {e}")

        # Generate image with pose
        output = pipe(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            image=pose_image,
            num_inference_steps=30,
            num_images_per_prompt=1,
            generator=torch.manual_seed(42)
        )

    else:
        # Load standard SDXL pipeline (no ControlNet)
        pipe = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True,
            safety_checker=None
        ).to("cuda")

        # VRAM optimizations
        pipe.enable_attention_slicing()
        pipe.enable_vae_slicing()
        pipe.enable_model_cpu_offload()
        try:
            pipe.enable_xformers_memory_efficient_attention()
        except Exception as e:
            print(f"⚠️ Warning: xformers attention not enabled: {e}")

        # Generate image without pose
        output = pipe(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            num_inference_steps=30,
            num_images_per_prompt=1,
            generator=torch.manual_seed(42)
        )

    image = output.images[0]
    image.save(args.output)
    print(f"✅ Image saved to {args.output}")

if __name__ == "__main__":
    main()