import os
import csv
import cv2
from PIL import Image
import numpy as np
from collections import defaultdict
import time

def enhance_spot_image(image_path, output_path):
    """
    Apply CLAHE enhancement to an image and save it
    """
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error loading image {image_path}")
        return None
    
    # Convert to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Split the LAB channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(10, 10))
    clahe_l = clahe.apply(l)
    
    # Merge the channels back
    clahe_lab = cv2.merge((clahe_l, a, b))
    
    # Convert back to BGR
    clahe_img = cv2.cvtColor(clahe_lab, cv2.COLOR_LAB2BGR)
    
    # Save the enhanced image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, clahe_img)
    
    return output_path

def check_gap_conditions(img_array, row, col):
    """
    Check whether the pixel meets GAP conditions:
    1. Grayscale value between 1-150 (inclusive)
    2. At least one adjacent pixel (up/down/left/right) has 25 contiguous pixels meeting the grayscale condition
    """
    height, width = img_array.shape
    
    # Check first condition
    pixel_value = img_array[row, col]
    if not (1 <= pixel_value <= 150):
        return 0
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Check second condition
    for dx, dy in directions:
        # Start from the adjacent pixel
        r, c = row + dx, col + dy
        
        # Skip if out of bounds
        if not (0 <= r < height and 0 <= c < width):
            continue
        
        # Count contiguous pixels that meet the grayscale condition
        count = 0
        current_r, current_c = r, c
        
        while (0 <= current_r < height and 0 <= current_c < width and 
               1 <= img_array[current_r, current_c] <= 150 and 
               count < 25):
            count += 1
            current_r += dx
            current_c += dy
        
        if count >= 25:
            return 1
    
    return 0

def process_images(input_directory):
    """
    Process all images in the directory whose filenames start with "Poly_"
    """
    # Create output directories
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup4"
    enhanced_directory = os.path.join(output_directory, "enhanced")
    csv_directory = os.path.join(output_directory, "csv")
    result_image_directory = os.path.join(output_directory, "result_images")
    
    os.makedirs(enhanced_directory, exist_ok=True)
    os.makedirs(csv_directory, exist_ok=True)
    os.makedirs(result_image_directory, exist_ok=True)
    
    # Get all image files with "Poly_" prefix
    image_files = [f for f in os.listdir(input_directory) 
                  if f.startswith("Poly_") and (f.lower().endswith('.png') or f.lower().endswith('.jpg'))]
    
    print(f"Found {len(image_files)} Poly_ images to process")
    
    for image_file in image_files:
        print(f"Processing {image_file}...")
        
        # Full paths
        image_path = os.path.join(input_directory, image_file)
        base_name = os.path.splitext(image_file)[0]
        enhanced_path = os.path.join(enhanced_directory, f"{base_name}_enhanced.png")
        csv_path = os.path.join(csv_directory, f"{base_name}_gap_analysis.csv")
        result_image_path = os.path.join(result_image_directory, f"{base_name}_gap_result.png")
        
        # Step 1: Apply CLAHE enhancement
        enhanced_image_path = enhance_spot_image(image_path, enhanced_path)
        if enhanced_image_path is None:
            continue
        
        # Step 2: Convert to grayscale and analyze pixels
        pil_img = Image.open(enhanced_path).convert('L')
        img_array = np.array(pil_img)
        height, width = img_array.shape
        
        # Prepare CSV data and result image
        csv_data = []
        result_img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Process each pixel
        for row in range(height):
            for col in range(width):
                gray_value = img_array[row, col]
                gap_flag = check_gap_conditions(img_array, row, col)
                
                # Store pixel data
                csv_data.append([row, col, gray_value, gap_flag])
                
                # Set result image pixel
                if gap_flag == 1:
                    result_img[row, col] = [0, 0, 0]  # Black for GAP=1
                else:
                    result_img[row, col] = [255, 255, 255]  # White for GAP=0
        
        # Save CSV file
        save_csv(csv_path, csv_data)
        
        # Save result image
        cv2.imwrite(result_image_path, result_img)
        
        print(f"Completed processing {image_file}")

def save_csv(csv_path, data):
    """
    Save pixel analysis data to CSV
    """
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Row', 'Column', 'Grayscale', 'GAP_Flag'])
        writer.writerows(data)

if __name__ == "__main__":
    start_time = time.time()
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    process_images(input_directory)
    end_time = time.time()
    print(f"Processed all images in {end_time - start_time:.2f} seconds!")
