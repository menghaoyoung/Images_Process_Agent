import os
import csv
import cv2
import numpy as np
from PIL import Image

# Constants
OUTPUT_DIR = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T3\backup9"
CLAHE_CLIP_LIMIT = 3.0
CLAHE_GRID_SIZE = (10, 10)
GRAY_MIN = 1
GRAY_MAX = 150
CONTIGUOUS_THRESHOLD = 25

def enhance_spot_image(img):
    """Apply CLAHE enhancement to the input image."""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP_LIMIT, tileGridSize=CLAHE_GRID_SIZE)
    cl = clahe.apply(l)
    enhanced_lab = cv2.merge((cl, a, b))
    enhanced_bgr = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    return enhanced_bgr

def check_gap_conditions(gray_array):
    """Determine GAP pixels based on grayscale values and contiguous neighbors."""
    # Create mask for grayscale range [1, 150]
    mask = (gray_array >= GRAY_MIN) & (gray_array <= GRAY_MAX)
    mask_uint8 = mask.astype(np.uint8) * 255
    
    # Find connected components (4-connectivity)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask_uint8, connectivity=4)
    
    # Identify large components (size >= 25)
    in_large_component = np.zeros_like(mask, dtype=bool)
    for label in range(1, num_labels):
        if stats[label, cv2.CC_STAT_AREA] >= CONTIGUOUS_THRESHOLD:
            in_large_component[labels == label] = True
    
    # Check neighbors for large components (top, bottom, left, right)
    neighbors_large = np.zeros_like(in_large_component, dtype=bool)
    # Top neighbor
    neighbors_large[1:, :] = np.logical_or(neighbors_large[1:, :], in_large_component[:-1, :])
    # Bottom neighbor
    neighbors_large[:-1, :] = np.logical_or(neighbors_large[:-1, :], in_large_component[1:, :])
    # Left neighbor
    neighbors_large[:, 1:] = np.logical_or(neighbors_large[:, 1:], in_large_component[:, :-1])
    # Right neighbor
    neighbors_large[:, :-1] = np.logical_or(neighbors_large[:, :-1], in_large_component[:, 1:])
    
    # GAP condition: in grayscale range AND has at least one neighbor in a large component
    gap_flags = np.logical_and(mask, neighbors_large).astype(np.uint8)
    return gap_flags

def save_csv(output_path, gray_array, gap_flags):
    """Save pixel analysis data to a CSV file."""
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Row", "Column", "Grayscale", "GAP_Flag"])
        rows, cols = gray_array.shape
        for r in range(rows):
            for c in range(cols):
                writer.writerow([r, c, gray_array[r, c], gap_flags[r, c]])

def process_images(input_directory):
    """Process all Poly_ images in the directory: enhance, analyze, and generate outputs."""
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # Process each image
    for filename in os.listdir(input_directory):
        if filename.startswith("Poly_") and (filename.lower().endswith('.png') or filename.lower().endswith('.jpg')):
            # Load image
            img_path = os.path.join(input_directory, filename)
            img = cv2.imread(img_path)
            if img is None:
                print(f"Warning: Could not read image {filename}. Skipping.")
                continue
            
            # Apply CLAHE enhancement and save
            enhanced_img = enhance_spot_image(img)
            base_name = os.path.splitext(filename)[0]
            enhanced_filename = f"{base_name}.png"
            enhanced_path = os.path.join(OUTPUT_DIR, enhanced_filename)
            cv2.imwrite(enhanced_path, enhanced_img)
            
            # Convert enhanced image to grayscale using PIL
            enhanced_rgb = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(enhanced_rgb)
            gray_pil = pil_img.convert('L')
            gray_array = np.array(gray_pil)
            
            # Identify GAP pixels
            gap_flags = check_gap_conditions(gray_array)
            
            # Generate CSV
            csv_filename = f"{base_name}_gap_analysis.csv"
            csv_path = os.path.join(OUTPUT_DIR, csv_filename)
            save_csv(csv_path, gray_array, gap_flags)
            
            # Generate binary image (GAP=1: black; GAP=0: white)
            binary_img = np.full((*gap_flags.shape, 3), 255, dtype=np.uint8)  # White background
            binary_img[gap_flags == 1] = [0, 0, 0]  # Black for GAP pixels
            bin_filename = f"{base_name}_gap.png"
            bin_path = os.path.join(OUTPUT_DIR, bin_filename)
            Image.fromarray(binary_img).save(bin_path)
    
    print("Processed all images!")

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    process_images(input_directory)
