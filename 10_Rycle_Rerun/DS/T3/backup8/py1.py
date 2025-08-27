import os
import sys
import csv
import cv2
import numpy as np
from PIL import Image

def enhance_spot_image(file_path, output_dir):
    """Read image, apply CLAHE enhancement, and save processed image"""
    img = cv2.imread(file_path)
    if img is None:
        print(f"Error reading image: {file_path}")
        return None

    # Convert to grayscale and apply CLAHE
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(10, 10))
    enhanced = clahe.apply(gray)
    
    # Save enhanced image
    filename = os.path.basename(file_path)
    output_path = os.path.join(output_dir, filename)
    cv2.imwrite(output_path, enhanced)
    return enhanced

def check_gap_conditions(gray_arr, i, j):
    """Check if pixel meets GAP conditions: 
    1) Grayscale between 1-150
    2) 25 contiguous pixels in one direction (up/down/left/right)"""
    height, width = gray_arr.shape
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    
    for dx, dy in directions:
        valid = True
        for step in range(1, 26):  # Check 25 contiguous pixels
            ni, nj = i + dx * step, j + dy * step
            # Boundary check
            if ni < 0 or ni >= height or nj < 0 or nj >= width:
                valid = False
                break
            # Grayscale value check
            if not (1 <= gray_arr[ni, nj] <= 150):
                valid = False
                break
        if valid:
            return True
    return False

def process_images(input_dir, output_dir):
    """Process all Poly_*.png/jpg images in input directory"""
    for filename in os.listdir(input_dir):
        if not filename.startswith("Poly_"):
            continue
        if not (filename.lower().endswith('.png') or filename.lower().endswith('.jpg')):
            continue
            
        file_path = os.path.join(input_dir, filename)
        enhanced_arr = enhance_spot_image(file_path, output_dir)
        if enhanced_arr is None:
            continue
            
        height, width = enhanced_arr.shape
        gap_flags = np.zeros((height, width), dtype=np.uint8)
        
        # Analyze each pixel
        for i in range(height):
            for j in range(width):
                # Condition 1: Grayscale value in range
                if 1 <= enhanced_arr[i, j] <= 150:
                    # Condition 2: Contiguous pixels check
                    if check_gap_conditions(enhanced_arr, i, j):
                        gap_flags[i, j] = 1
        
        # Save outputs
        save_csv(enhanced_arr, gap_flags, filename, output_dir)
        generate_gap_image(gap_flags, filename, output_dir)
        
def save_csv(gray_arr, gap_flags, filename, output_dir):
    """Save pixel analysis to CSV file"""
    base_name = os.path.splitext(filename)[0]
    csv_path = os.path.join(output_dir, f"{base_name}_gap_analysis.csv")
    
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['row', 'column', 'grayscale_value', 'GAP_flag'])
        
        for i in range(gray_arr.shape[0]):
            for j in range(gray_arr.shape[1]):
                writer.writerow([i, j, gray_arr[i, j], gap_flags[i, j]])

def generate_gap_image(gap_flags, filename, output_dir):
    """Create binary mask image from gap flags"""
    base_name = os.path.splitext(filename)[0]
    img_path = os.path.join(output_dir, f"{base_name}_gap_mask.png")
    
    # Create RGB image: GAP=1 -> Black (0,0,0), GAP=0 -> White (255,255,255)
    img_arr = np.zeros((*gap_flags.shape, 3), dtype=np.uint8)
    img_arr[gap_flags == 1] = [0, 0, 0]    # Black for GAP pixels
    img_arr[gap_flags == 0] = [255, 255, 255]  # White for non-GAP
    
    Image.fromarray(img_arr, 'RGB').save(img_path)

if __name__ == "__main__":
    # Configure paths
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T3\backup8"
    
    # Handle command line argument
    if len(sys.argv) > 1:
        input_directory = sys.argv[1]
    
    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Process images
    process_images(input_directory, output_directory)
    print("Processed all images!")
