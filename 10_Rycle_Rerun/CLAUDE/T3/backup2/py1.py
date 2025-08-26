import os
import csv
import cv2
from PIL import Image
import numpy as np
from collections import defaultdict
import time

def enhance_spot_image(image_path, output_path):
    """Apply CLAHE enhancement to an image and save it."""
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    
    # Convert to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # Split the LAB image into L, A, and B channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to the L channel
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(10, 10))
    clahe_l = clahe.apply(l)
    
    # Merge the CLAHE-enhanced L channel with the original A and B channels
    clahe_lab = cv2.merge((clahe_l, a, b))
    
    # Convert back to BGR color space
    clahe_bgr = cv2.cvtColor(clahe_lab, cv2.COLOR_LAB2BGR)
    
    # Save the CLAHE-enhanced image
    cv2.imwrite(output_path, clahe_bgr)
    
    return output_path

def check_gap_conditions(gray_image, row, col, threshold=160):
    """
    Check if a pixel meets the GAP conditions:
    1. Grayscale value between 1-160 (inclusive)
    2. At least one adjacent pixel (up/down/left/right) has 25 contiguous pixels meeting the grayscale condition
    """
    height, width = gray_image.shape
    
    # Check condition 1: Grayscale value between 1-160
    pixel_value = gray_image[row, col]
    if not (1 <= pixel_value <= threshold):
        return 0
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Check condition 2
    for dr, dc in directions:
        r, c = row + dr, col + dc
        
        # Skip if out of bounds
        if not (0 <= r < height and 0 <= c < width):
            continue
        
        # Check if the adjacent pixel is within the grayscale range
        if 1 <= gray_image[r, c] <= threshold:
            # Count contiguous pixels in this direction
            count = 1
            for i in range(2, 26):  # Check up to 25 pixels
                next_r, next_c = row + i*dr, col + i*dc
                
                # Break if out of bounds or not meeting the condition
                if not (0 <= next_r < height and 0 <= next_c < width) or not (1 <= gray_image[next_r, next_c] <= threshold):
                    break
                
                count += 1
            
            # If we found 25 contiguous pixels, return 1
            if count >= 25:
                return 1
    
    return 0

def process_images(input_directory):
    """Process all images with 'Poly_' prefix in the directory."""
    # Create output directories if they don't exist
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup2"
    clahe_dir = os.path.join(output_dir, "clahe_images")
    csv_dir = os.path.join(output_dir, "csv_files")
    result_img_dir = os.path.join(output_dir, "result_images")
    
    for directory in [output_dir, clahe_dir, csv_dir, result_img_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Get all image files with 'Poly_' prefix
    image_files = [f for f in os.listdir(input_directory) 
                  if f.startswith('Poly_') and (f.lower().endswith('.png') or f.lower().endswith('.jpg'))]
    
    print(f"Found {len(image_files)} images to process.")
    
    for image_file in image_files:
        print(f"Processing {image_file}...")
        
        # Full path to the original image
        image_path = os.path.join(input_directory, image_file)
        
        # Paths for output files
        base_name = os.path.splitext(image_file)[0]
        clahe_path = os.path.join(clahe_dir, f"{base_name}_clahe.png")
        csv_path = os.path.join(csv_dir, f"{base_name}_gap_analysis.csv")
        result_img_path = os.path.join(result_img_dir, f"{base_name}_result.png")
        
        # Step 1: Apply CLAHE enhancement
        enhance_spot_image(image_path, clahe_path)
        
        # Step 2: Process the CLAHE-enhanced image
        process_new_images(clahe_path, csv_path, result_img_path)

def process_new_images(clahe_image_path, csv_path, result_img_path):
    """Process CLAHE-enhanced images to identify GAP pixels and generate output files."""
    # Open the CLAHE-enhanced image with PIL
    pil_image = Image.open(clahe_image_path).convert('L')  # Convert to grayscale
    gray_array = np.array(pil_image)
    
    height, width = gray_array.shape
    
    # Create a new image for the result
    result_image = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background
    
    # Open CSV file for writing
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Row', 'Column', 'Grayscale Value', 'GAP Flag'])
        
        # Process each pixel
        for row in range(height):
            for col in range(width):
                gray_value = gray_array[row, col]
                gap_flag = check_gap_conditions(gray_array, row, col)
                
                # Write to CSV
                writer.writerow([row, col, int(gray_value), gap_flag])
                
                # Update result image
                if gap_flag == 1:
                    result_image[row, col] = [0, 0, 0]  # Black for GAP=1
    
    # Save the result image
    cv2.imwrite(result_img_path, result_image)

def save_csv(data, csv_path):
    """Save pixel analysis data to a CSV file."""
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Row', 'Column', 'Grayscale Value', 'GAP Flag'])
        
        for row, col, gray_value, gap_flag in data:
            writer.writerow([row, col, gray_value, gap_flag])

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    start_time = time.time()
    process_images(input_directory)
    end_time = time.time()
    print(f"Processed all the images! Time taken: {end_time - start_time:.2f} seconds")
