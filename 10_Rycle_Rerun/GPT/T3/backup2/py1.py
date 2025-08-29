import os
import csv
import cv2
from PIL import Image
import numpy as np
from collections import deque
import time

# Set output directory
OUTPUT_DIR = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T3\backup2"

def enhance_spot_image(img):
    # Create CLAHE object with clipLimit=3, tileGridSize=(10, 10)
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(10, 10))
    if len(img.shape) == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    enhanced = clahe.apply(gray)
    return enhanced

def check_gap_conditions(grayscale_img, row, col):
    """
    (1) Grayscale value between 1–150 (inclusive) 
    (2) At least one adjacent pixel (up/down/left/right) has 25 contiguous pixels (in that direction) meeting the grayscale condition
    """
    height, width = grayscale_img.shape
    val = grayscale_img[row, col]
    if val < 1 or val > 150:
        return 0

    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        count = 0
        for k in range(1, 26):
            nr = row + dr * k
            nc = col + dc * k
            if 0 <= nr < height and 0 <= nc < width:
                nval = grayscale_img[nr, nc]
                if 1 <= nval <= 150:
                    count += 1
                else:
                    break
            else:
                break
        if count == 25:
            return 1
    return 0

def process_images(input_directory):
    supported_ext = ('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG')
    filenames = [f for f in os.listdir(input_directory) if f.startswith("Poly_") and f.endswith(supported_ext)]

    print(f"Found {len(filenames)} images with 'Poly_' prefix.")

    for fname in filenames:
        img_path = os.path.join(input_directory, fname)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load image {fname}")
            continue

        # CLAHE enhancement
        enhanced = enhance_spot_image(img)

        # Save CLAHE-enhanced image
        base_name, _ = os.path.splitext(fname)
        clahe_img_name = f"{base_name}_CLAHE.png"
        clahe_img_path = os.path.join(OUTPUT_DIR, clahe_img_name)
        cv2.imwrite(clahe_img_path, enhanced)
        print(f"Saved CLAHE-enhanced image to {clahe_img_path}")

        # Process enhanced image with Pillow
        pil_img = Image.fromarray(enhanced)
        grayscale_img = np.array(pil_img)  # Already grayscale

        gap_flags = np.zeros_like(grayscale_img, dtype=np.uint8)
        height, width = grayscale_img.shape

        csv_records = []

        print(f"Processing GAP detection for {fname} ...")
        for row in range(height):
            for col in range(width):
                val = int(grayscale_img[row, col])
                flag = check_gap_conditions(grayscale_img, row, col)
                gap_flags[row, col] = flag
                csv_records.append([row, col, val, flag])

        # Save CSV
        csv_fname = f"{base_name}_gap_analysis.csv"
        csv_path = os.path.join(OUTPUT_DIR, csv_fname)
        with open(csv_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['row', 'col', 'grayscale', 'GAP_flag'])
            csvwriter.writerows(csv_records)
        print(f"Wrote CSV analysis to {csv_path}")

        # Generate binary gap image
        output_img = np.where(gap_flags == 1, 0, 255).astype(np.uint8)
        output_img_rgb = np.stack([output_img]*3, axis=-1)  # Make RGB
        out_img_fname = f"{base_name}_GAP_flag.png"
        out_img_path = os.path.join(OUTPUT_DIR, out_img_fname)
        Image.fromarray(output_img_rgb).save(out_img_path)
        print(f"Wrote GAP-flagged image to {out_img_path}")

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    process_images(input_directory)
    print("Proceed all the images！")
