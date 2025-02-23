import os
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image


def main():
    # Set the cache directory for all downloads
    cache_dir = "/Data/my_project_env2/huggingface_cache"
    os.environ["TRANSFORMERS_CACHE"] = cache_dir
    os.environ["HF_HOME"] = cache_dir
    os.environ["TORCH_HOME"] = cache_dir

    # Path to your image of the Rubik's cube
    image_path = "images/klein_bottle.jpg"
    image = Image.open(image_path).convert("RGB")

    # Load BLIP2 model with custom cache directory
    model_name = "Salesforce/blip2-opt-2.7b"
    processor = Blip2Processor.from_pretrained(model_name, cache_dir=cache_dir)
    model = Blip2ForConditionalGeneration.from_pretrained(model_name, cache_dir=cache_dir)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # Generate a caption without a prompt
    inputs = processor(image, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)
    print("Generated Description:", description)

    # Write the description to a file for use by granite_code.py
    with open("description.txt", "w") as f:
        f.write(description)


if __name__ == "__main__":
    main()
