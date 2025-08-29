import os
import csv
import cv2
from PIL import Image
import numpy as np

def enhance_spot_image(img, clipLimit=3, tileGridSize=(10, 10)):
    """Apply CLAHE enhancement to the input image."""
    if len(img.shape) == 3:  # color image
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
    enhanced = clahe.apply(img_gray)
    return enhanced

def check_gap_conditions(gray_img, row, col):
    """
    Check if the pixel at (row, col) meets GAP condition:
    (1) Grayscale value between 1-150 (inclusive)
    (2) At least one direction (up/down/left/right) has 25 contiguous pixels
        meeting the grayscale value condition (1-150 inclusive)
    Return: 1 if GAP, 0 otherwise
    """
    h, w = gray_img.shape
    if not (1 <= gray_img[row, col] <= 150):
        return 0

    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # up, down, left, right
    for dr, dc in directions:
        count = 0
        for k in range(1, 26):  # 1 to 25
            nr, nc = row + dr * k, col + dc * k
            if 0 <= nr < h and 0 <= nc < w:
                if 1 <= gray_img[nr, nc] <= 150:
                    count += 1
                else:
                    break
            else:
                break
        if count == 25:
            return 1
    return 0

def save_csv(csv_path, data):
    """Save pixel analysis data to CSV."""
    with open(csv_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['row', 'column', 'grayscale', 'GAP_flag'])
        writer.writerows(data)

def process_new_images(output_img_path, gap_flags):
    """
    Save new PNG image:
    - GAP_flag==1: black (0,0,0)
    - GAP_flag==0: white (255,255,255)
    """
    h, w = gap_flags.shape
    new_img = np.ones((h, w, 3), dtype=np.uint8) * 255
    new_img[gap_flags == 1] = [0, 0, 0]
    new_img_pil = Image.fromarray(new_img)
    new_img_pil.save(output_img_path)

def process_images(input_directory):
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T3\backup1"
    os.makedirs(output_directory, exist_ok=True)
    img_files = [f for f in os.listdir(input_directory) if f.lower().startswith("poly_") and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"Found {len(img_files)} images to process.")
    for img_name in img_files:
        img_path = os.path.join(input_directory, img_name)
        print(f"Processing: {img_path}")
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to read {img_path}, skipping.")
            continue
        # Step 1: CLAHE enhancement
        enhanced = enhance_spot_image(img, clipLimit=3, tileGridSize=(10, 10))
        enhanced_img_name = os.path.splitext(img_name)[0] + "_CLAHE.png"
        enhanced_img_path = os.path.join(output_directory, enhanced_img_name)
        cv2.imwrite(enhanced_img_path, enhanced)
        print(f"Saved CLAHE image: {enhanced_img_path}")

        # Step 2: Convert to grayscale with PIL and extract values
        pil_img = Image.fromarray(enhanced)
        gray_img = np.array(pil_img)
        h, w = gray_img.shape
        gap_flags = np.zeros_like(gray_img, dtype=np.uint8)
        data_rows = []

        # Step 3: Per-pixel analysis
        for row in range(h):
            for col in range(w):
                gray_value = gray_img[row, col]
                gap_flag = check_gap_conditions(gray_img, row, col)
                gap_flags[row, col] = gap_flag
                data_rows.append([row, col, int(gray_value), int(gap_flag)])

        # Step 4: Save CSV
        csv_name = os.path.splitext(img_name)[0] + "_gap_analysis.csv"
        csv_path = os.path.join(output_directory, csv_name)
        save_csv(csv_path, data_rows)
        print(f"Saved CSV: {csv_path}")

        # Step 5: Save new visualization image
        new_img_name = os.path.splitext(img_name)[0] + "_GAP_visual.png"
        new_img_path = os.path.join(output_directory, new_img_name)
        process_new_images(new_img_path, gap_flags)
        print(f"Saved GAP visualization image: {new_img_path}")

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    process_images(input_directory)
    print("Proceed all the images！")
