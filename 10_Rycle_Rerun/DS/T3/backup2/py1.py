import os
import csv
import cv2
import numpy as np
from PIL import Image
import sys

def enhance_spot_image(img):
    """Apply CLAHE enhancement to a grayscale image."""
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(10, 10))
    enhanced = clahe.apply(img)
    return enhanced

def check_gap_conditions(gray_array):
    """Identify GAP pixels based on grayscale value and adjacent contiguous regions."""
    h, w = gray_array.shape
    mask = (gray_array >= 1) & (gray_array <= 150)
    mask_uint8 = mask.astype(np.uint8) * 255
    
    # Find connected components (4-connectivity)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask_uint8, connectivity=4)
    
    # Identify large components (size >= 25)
    large_labels = set()
    for label in range(1, num_labels):  # Skip background (label=0)
        if stats[label, cv2.CC_STAT_AREA] >= 25:
            large_labels.add(label)
    
    # Check neighbors for large components
    gap_flags = np.zeros((h, w), dtype=np.uint8)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    
    for i in range(h):
        for j in range(w):
            if mask[i, j]:  # Condition (1)
                for dx, dy in directions:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < h and 0 <= nj < w:
                        neighbor_label = labels[ni, nj]
                        if neighbor_label in large_labels:
                            gap_flags[i, j] = 1
                            break
    return gap_flags

def save_csv(csv_path, gray_array, gap_flags):
    """Save pixel analysis data to a CSV file."""
    h, w = gray_array.shape
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['row', 'column', 'grayscale', 'gap_flag'])
        for i in range(h):
            for j in range(w):
                writer.writerow([i, j, gray_array[i, j], gap_flags[i, j]])

def create_gap_highlight_image(gap_flags):
    """Generate a black-and-white image highlighting GAP pixels."""
    h, w = gap_flags.shape
    bw_image = np.full((h, w, 3), 255, dtype=np.uint8)  # White background
    bw_image[gap_flags == 1] = [0, 0, 0]  # Black for GAP pixels
    return Image.fromarray(bw_image, 'RGB')

def process_images(input_dir):
    """Process all Poly_ images in the input directory."""
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T3\backup9"
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.startswith("Poly_") and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(input_dir, filename)
            img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
                
            # Process image
            base_name = os.path.splitext(filename)[0]
            enhanced = enhance_spot_image(img)
            gap_flags = check_gap_conditions(enhanced)
            
            # Save outputs
            csv_path = os.path.join(output_dir, f"{base_name}_gap_analysis.csv")
            save_csv(csv_path, enhanced, gap_flags)
            
            highlight_img = create_gap_highlight_image(gap_flags)
            highlight_path = os.path.join(output_dir, f"{base_name}_gap_highlight.png")
            highlight_img.save(highlight_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python py1.py <input_directory>")
        sys.exit(1)
        
    input_directory = sys.argv[1]
    process_images(input_directory)
    print("Processed all images!")
