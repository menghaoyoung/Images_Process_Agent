import os
import csv
import cv2
from PIL import Image
import numpy as np

# Output directory
OUTPUT_DIR = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T3\backup6"

def enhance_spot_image(img):
    """Apply CLAHE enhancement to a grayscale image."""
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(10, 10))
    return clahe.apply(img)

def check_gap_conditions(arr, i, j):
    """Check if a pixel meets GAP conditions (grayscale range and contiguous neighbors)."""
    # Condition 1: Grayscale value between 1 and 150 (inclusive)
    if not (1 <= arr[i, j] <= 150):
        return 0
    
    # Condition 2: Check for 25 contiguous pixels in any direction
    directions = [
        (0, 1),   # Right
        (0, -1),  # Left
        (1, 0),   # Down
        (-1, 0)   # Up
    ]
    
    for di, dj in directions:
        # Check contiguous pixels in this direction
        count = 0
        ni, nj = i + di, j + dj
        # Verify we have 25 contiguous valid pixels
        for step in range(25):
            if (ni < 0 or ni >= arr.shape[0] or 
                nj < 0 or nj >= arr.shape[1] or 
                not (1 <= arr[ni, nj] <= 150)):
                break
            count += 1
            ni += di
            nj += dj
        if count >= 25:
            return 1
    return 0

def save_csv(base, img, gap_flags):
    """Save pixel analysis data to a CSV file."""
    csv_path = os.path.join(OUTPUT_DIR, f"{base}_gap_analysis.csv")
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['row', 'col', 'grayscale', 'gap_flag'])
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                writer.writerow([i, j, img[i, j], gap_flags[i, j]])

def process_new_images(base, gap_flags):
    """Generate a PNG image highlighting GAP pixels."""
    height, width = gap_flags.shape
    highlight_img = np.zeros((height, width, 3), dtype=np.uint8)
    # Set GAP pixels (flag=1) to black and others to white
    highlight_img[gap_flags == 1] = [0, 0, 0]
    highlight_img[gap_flags == 0] = [255, 255, 255]
    # Save as PNG
    img_path = os.path.join(OUTPUT_DIR, f"{base}_gap_highlight.png")
    cv2.imwrite(img_path, highlight_img)

def process_images(input_directory):
    """Process all Poly_ images in the input directory."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(input_directory):
        if filename.startswith("Poly_") and filename.lower().endswith(('.png', '.jpg')):
            # Read and process the image
            img_path = os.path.join(input_directory, filename)
            img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img_gray is None:
                continue
            
            # Apply CLAHE enhancement
            clahe_img = enhance_spot_image(img_gray)
            base_name = os.path.splitext(filename)[0]
            
            # Save CLAHE-enhanced image
            clahe_path = os.path.join(OUTPUT_DIR, f"{base_name}_clahe.png")
            cv2.imwrite(clahe_path, clahe_img)
            
            # Process with PIL: Read saved CLAHE image and convert to grayscale
            pil_img = Image.open(clahe_path).convert('L')
            clahe_img = np.array(pil_img)
            
            # Analyze pixels for GAP conditions
            height, width = clahe_img.shape
            gap_flags = np.zeros((height, width), dtype=np.uint8)
            for i in range(height):
                for j in range(width):
                    gap_flags[i, j] = check_gap_conditions(clahe_img, i, j)
            
            # Generate outputs
            save_csv(base_name, clahe_img, gap_flags)
            process_new_images(base_name, gap_flags)

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    process_images(input_directory)
    print("Proceed all the images！")
