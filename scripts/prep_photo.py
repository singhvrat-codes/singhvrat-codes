import sys
import os
import cv2
import numpy as np
from PIL import Image

def process_photo(input_path, output_path="data/source-prepped.png"):
    print(f"Loading image from {input_path}...")
    
    # 1. Try background removal with rembg, fallback to opencv thresholding if rembg not installed/fails
    has_rembg = False
    try:
        from rembg import remove
        has_rembg = True
    except ImportError:
        print("rembg not installed; using OpenCV foreground separation fallback.")

    if has_rembg:
        with open(input_path, 'rb') as i:
            input_bytes = i.read()
            output_bytes = remove(input_bytes)
        img_np = cv2.imdecode(np.frombuffer(output_bytes, np.uint8), cv2.IMREAD_UNCHANGED)
        
        # If image has alpha channel, composite onto pure white
        if img_np.shape[2] == 4:
            alpha = img_np[:, :, 3] / 255.0
            rgb = img_np[:, :, :3]
            white_bg = np.ones_like(rgb, dtype=np.uint8) * 255
            for c in range(3):
                rgb[:, :, c] = rgb[:, :, c] * alpha + white_bg[:, :, c] * (1 - alpha)
            gray = cv2.cvtColor(rgb.astype(np.uint8), cv2.COLOR_BGR2GRAY)
        else:
            gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    else:
        # Fallback: Read image as grayscale
        gray = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        if gray is None:
            raise FileNotFoundError(f"Could not open image file: {input_path}")

    # 2. Boost local contrast using OpenCV CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Ensure target output folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, enhanced)
    print(f"Successfully prepped photo saved to {output_path}")

def generate_sample_photo(path="source-photo.jpg"):
    """Generate a clean synthetic portrait if no input photo is provided."""
    img = np.ones((400, 300, 3), dtype=np.uint8) * 240
    # Draw head
    cv2.circle(img, (150, 150), 90, (80, 80, 80), -1)
    # Draw eyes
    cv2.circle(img, (120, 130), 12, (255, 255, 255), -1)
    cv2.circle(img, (180, 130), 12, (255, 255, 255), -1)
    cv2.circle(img, (120, 130), 5, (30, 30, 30), -1)
    cv2.circle(img, (180, 130), 5, (30, 30, 30), -1)
    # Draw smile
    cv2.ellipse(img, (150, 180), (35, 20), 0, 0, 180, (40, 40, 40), 6)
    # Draw shoulders
    cv2.ellipse(img, (150, 330), (120, 80), 0, 180, 360, (60, 60, 60), -1)
    
    cv2.imwrite(path, img)
    print(f"Generated sample portrait photo at {path}")

if __name__ == "__main__":
    photo_file = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    if not os.path.exists(photo_file):
        generate_sample_photo(photo_file)
    process_photo(photo_file)
