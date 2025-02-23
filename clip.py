import sys
import json
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Load CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Import JSON knowledge base
with open("shape_knowledge.json", "r") as f:
    shape_knowledge = json.load(f)

# Modified detection function
def detect_shapes(image_path):
    # PIL supports PNG images, so you can process PNGs as well.
    image = Image.open(image_path)
    inputs = processor(
        text=list(shape_knowledge.keys()),
        images=image,
        return_tensors="pt",
        padding=True
    )

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1).squeeze()

    return {
        shape_name: {
            "confidence": prob.item(),
            "description": shape_knowledge[shape_name]
        }
        for shape_name, prob in zip(shape_knowledge.keys(), probs)
        if prob > 0.2  # Confidence threshold
    }

if __name__ == "__main__":
    # Expect the image path as the first command-line argument
    if len(sys.argv) < 2:
        print("Usage: python clip.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    results = detect_shapes(image_path)

    if not results:
        print("No shapes detected with sufficient confidence.")
        sys.exit(0)

    # Print all detected shapes and their scores
    print("Detected shapes:")
    for shape, data in results.items():
        print(f"{shape} ({data['confidence']:.2f}): {data['description']}")

    # Select the shape with the highest confidence
    best_shape, best_data = max(results.items(), key=lambda item: item[1]["confidence"])

    # Write the description of the best-scoring shape to a file for granite_code.py to use
    with open("clip_description.txt", "w") as f:
        f.write(best_data["description"])

    print("\nBest shape:")
    print(f"{best_shape} ({best_data['confidence']:.2f}): {best_data['description']}")
