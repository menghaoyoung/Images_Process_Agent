import os
import csv
import cv2
import numpy as np
from PIL import Image
import sys

# Constants
OUTPUT_DIRECTORY = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T3\backup7"
CLAHE_CLIP_LIMIT = 3.0
CLAHE_GRID_SIZE = (10, 10)
GAP_GRAY_MIN = 1
GAP_GRAY_MAX = 150
CONTIGUOUS_REQUIREMENT = 25

def enhance_spot_image(img):
    """Apply CLAHE enhancement to an input image"""
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP_LIMIT, tileGridSize=CLAHE_GRID_SIZE)
    enhanced = clahe.apply(gray)
    return enhanced

def check_gap_conditions(i, j, gray_img):
    """Check if pixel meets GAP conditions"""
    height, width = gray_img.shape
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
    
    for dx, dy in directions:
        ni, nj = i + dx, j + dy  # Adjacent pixel coordinates
        
        # Skip if adjacent pixel is out of bounds
        if ni < 0 or ni >= height or nj < 0 or nj >= width:
            continue
            
        # Skip if adjacent pixel doesn't meet grayscale condition
        if not (GAP_GRAY_MIN <= gray_img[ni, nj] <= GAP_GRAY_MAX):
            continue
            
        count = 1  # Start counting from adjacent pixel
        # Check continuous pixels in current direction
        for step in range(1, CONTIGUOUS_REQUIREMENT):
            nni, nnj = ni + dx * step, nj + dy * step
            if nni < 0 or nni >= height or nnj < 0 or nnj >= width:
                break
            if not (GAP_GRAY_MIN <= gray_img[nni, nnj] <= GAP_GRAY_MAX):
                break
            count += 1
            if count >= CONTIGUOUS_REQUIREMENT:
                return True
    return False

def save_csv(filename, rows):
    """Save pixel data to CSV file"""
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['row', 'column', 'grayscale_value', 'gap_flag'])
        writer.writerows(rows)

def process_images(input_directory):
    """Process all images in the input directory"""
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    
    # Process each image with Poly_ prefix
    for filename in os.listdir(input_directory):
        if filename.startswith("Poly_") and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Processing image: {filename}")
            filepath = os.path.join(input_directory, filename)
            
            # Read and enhance image
            img = cv2.imread(filepath)
            if img is None:
                print(f"  Error loading image: {filename}")
                continue
                
            enhanced_gray = enhance_spot_image(img)
            
            # Save enhanced image
            basename = os.path.splitext(filename)[0]
            enhanced_path = os.path.join(OUTPUT_DIRECTORY, f"{basename}_enhanced.png")
            cv2.imwrite(enhanced_path, enhanced_gray)
            
            # Process with PIL
            pil_img = Image.open(enhanced_path).convert('L')
            gray_array = np.array(pil_img)
            height, width = gray_array.shape
            
            # Process pixels
            csv_rows = []
            gap_flags = np.zeros((height, width), dtype=np.uint8)
            
            for i in range(height):
                for j in range(width):
                    gray_val = gray_array[i, j]
                    gap_flag = 0
                    
                    # Check condition 1: Grayscale in range
                    if GAP_GRAY_MIN <= gray_val <= GAP_GRAY_MAX:
                        # Check condition 2: Contiguous pixels
                        if check_gap_conditions(i, j, gray_array):
                            gap_flag = 1
                            gap_flags[i, j] = 1
                    
                    csv_rows.append([i, j, gray_val, gap_flag])
            
            # Save CSV
            csv_filename = os.path.join(OUTPUT_DIRECTORY, f"{basename}_gap_analysis.csv")
            save_csv(csv_filename, csv_rows)
            
            # Create and save gap visualization
            gap_img = np.full((height, width, 3), 255, dtype=np.uint8)  # White background
            gap_img[gap_flags == 1] = [0, 0, 0]  # Black for GAP pixels
            gap_image_path = os.path.join(OUTPUT_DIRECTORY, f"{basename}_gap_flags.png")
            cv2.imwrite(gap_image_path, gap_img)
            
            print(f"  Completed processing: {filename}")

def process_new_images():
    """Function defined in framework but not used in this implementation"""
    pass

if __name__ == "__main__":
    # Get input directory from command line or use default
    if len(sys.argv) > 1:
        input_directory = sys.argv[1]
    else:
        input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    
    process_images(input_directory)
    print("Processed all images!")
