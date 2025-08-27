import os
import csv
import cv2
from PIL import Image
import numpy as np
import time

def apply_clahe(image_path, output_dir):
    img = cv2.imread(image_path)
    if img is None:
        return None, None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(10, 10))
    enhanced_gray = clahe.apply(gray)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    clahe_path = os.path.join(output_dir, base_name + '_clahe.png')
    cv2.imwrite(clahe_path, enhanced_gray)
    return enhanced_gray, base_name

def compute_gap_mask(enhanced_gray):
    mask = (enhanced_gray >= 1) & (enhanced_gray <= 150)
    mask_uint8 = mask.astype(np.uint8) * 255
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask_uint8, connectivity=4)
    large_component_map = np.zeros_like(mask, dtype=bool)
    for label in range(1, num_labels):
        if stats[label, cv2.CC_STAT_AREA] >= 25:
            large_component_map[labels == label] = True
    height, width = enhanced_gray.shape
    gap_flag = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            if not mask[i, j]:
                continue
            neighbors = []
            if i > 0: neighbors.append((i-1, j))
            if i < height-1: neighbors.append((i+1, j))
            if j > 0: neighbors.append((i, j-1))
            if j < width-1: neighbors.append((i, j+1))
            for ni, nj in neighbors:
                if large_component_map[ni, nj]:
                    gap_flag[i, j] = 1
                    break
    return gap_flag

def save_csv(enhanced_gray, gap_flag, base_name, output_dir):
    height, width = enhanced_gray.shape
    csv_path = os.path.join(output_dir, base_name + '_gap_analysis.csv')
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['row', 'column', 'grayscale_value', 'GAP_flag'])
        for i in range(height):
            for j in range(width):
                writer.writerow([i, j, enhanced_gray[i, j], gap_flag[i, j]])

def create_gap_image(gap_flag, base_name, output_dir):
    height, width = gap_flag.shape
    img_out = np.zeros((height, width, 3), dtype=np.uint8)
    img_out[gap_flag == 1] = [0, 0, 0]       # GAP pixels: black
    img_out[gap_flag == 0] = [255, 255, 255] # Non-GAP: white
    image_pil = Image.fromarray(img_out)
    image_pil.save(os.path.join(output_dir, base_name + '_gap.png'))

def process_images(input_directory):
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T3\backup5"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    processed_files = []
    for filename in os.listdir(input_directory):
        if filename.startswith("Poly_") and filename.lower().endswith(('.png', '.jpg')):
            filepath = os.path.join(input_directory, filename)
            enhanced_gray, base_name = apply_clahe(filepath, output_dir)
            if enhanced_gray is None:
                continue
            gap_flag = compute_gap_mask(enhanced_gray)
            save_csv(enhanced_gray, gap_flag, base_name, output_dir)
            create_gap_image(gap_flag, base_name, output_dir)
            processed_files.append(base_name)
    return processed_files

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    process_images(input_directory)
    print("Processed all images!")
