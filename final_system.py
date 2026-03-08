import hashlib
from PIL import Image
import io
import os

LEDGER = {
    "xray_chest.png": "ff91cc4ec1e5606e64a39f8e7a49bcb4eaa7dd8ce3a4a4f54401d2ba09b0cdda",
    "xray_neck.png": "7afedc0297491a547a17c70597713d58f708f8062d79697a27bd84be289fcb7c"
}

def generate_attack(image_name):
    path = f"images/{image_name}"
    output = f"images/attacked_{image_name}"
    if os.path.exists(path):
        img = Image.open(path).convert('RGB')
        pixels = img.load()
        r, g, b = pixels[0, 0]
        pixels[0, 0] = (min(r + 1, 255), g, b)
        img.save(output)
        return output

def calculate_hash(image_path):
    with Image.open(image_path) as img:
        buf = io.BytesIO()
        img.save(buf, format=img.format)
        return hashlib.sha256(buf.getvalue()).hexdigest()

def ai_diagnosis(image_name):
    if "chest" in image_name:
        return "Normal (No Pneumonia detected)"
    return "Healthy Bone Structure"

def run_system(image_name, test_attack=True):
    print(f"\n--- Processing: {image_name} ---")
    
    if test_attack:
        target_path = generate_attack(image_name)
        print("Status: Testing Attacked Image...")
    else:
        target_path = f"images/{image_name}"
        print("Status: Testing Original Image...")

    current_hash = calculate_hash(target_path)
    original_hash = LEDGER[image_name]

    if current_hash == original_hash:
        print("Result: Hash Matches (Secure)")
        print(f"AI Model Output: {ai_diagnosis(image_name)}")
    else:
        print("Result: Hash Mismatch (REJECTED)")
        print("Action: System Aborted.")

if __name__ == "__main__":
    run_system("xray_chest.png", test_attack=True)
    run_system("xray_chest.png", test_attack=False)
