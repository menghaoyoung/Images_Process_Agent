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
        print(f"Failed to read image: {image_path}")
        return None
    
    # Convert to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Split LAB channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(10, 10))
    cl = clahe.apply(l)
    
    # Merge channels back
    limg = cv2.merge((cl, a, b))
    
    # Convert back to BGR
    enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    # Save the enhanced image
    cv2.imwrite(output_path, enhanced)
    
    return enhanced

def check_gap_conditions(gray_img, row, col, threshold_min=1, threshold_max=150, contiguous_count=25):
    """
    Check if a pixel meets the GAP conditions:
    1. Grayscale value between threshold_min and threshold_max (inclusive)
    2. At least one adjacent pixel (up/down/left/right) has contiguous_count pixels 
       meeting the grayscale condition
    """
    height, width = gray_img.shape
    
    # Check first condition - grayscale value range
    pixel_value = gray_img[row, col]
    if not (threshold_min <= pixel_value <= threshold_max):
        return False, pixel_value
    
    # Directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # Check second condition for each direction
    for dr, dc in directions:
        count = 0
        r, c = row, col
        
        # Count contiguous pixels in this direction
        for _ in range(contiguous_count):
            r += dr
            c += dc
            
            # Check if position is valid
            if 0 <= r < height and 0 <= c < width:
                if threshold_min <= gray_img[r, c] <= threshold_max:
                    count += 1
                else:
                    break
            else:
                break
        
        # If we found enough contiguous pixels in this direction
        if count >= contiguous_count:
            return True, pixel_value
    
    return False, pixel_value

def process_new_images(original_image_path, gap_data, output_image_path):
    """
    Generate a new PNG image highlighting GAP points
    """
    # Get original image dimensions
    img = Image.open(original_image_path)
    width, height = img.size
    
    # Create a new white image
    new_img = Image.new('RGB', (width, height), color=(255, 255, 255))
    pixels = new_img.load()
    
    # Set pixels based on GAP flag
    for (row, col), (gray_value, gap_flag) in gap_data.items():
        if gap_flag == 1:
            pixels[col, row] = (0, 0, 0)  # Black for GAP=1
        else:
            pixels[col, row] = (255, 255, 255)  # White for GAP=0
    
    # Save the new image
    new_img.save(output_image_path)

def save_csv(image_name, gap_data, output_csv_path):
    """
    Save pixel analysis data to CSV
    """
    with open(output_csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write header
        csvwriter.writerow(['Row', 'Column', 'Grayscale_Value', 'GAP_Flag'])
        
        # Write data
        for (row, col), (gray_value, gap_flag) in gap_data.items():
            csvwriter.writerow([row, col, gray_value, gap_flag])

def process_images(input_directory):
    """
    Process all images in the directory whose filenames start with "Poly_"
    """
    # Create output directory if it doesn't exist
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup5"
    os.makedirs(output_directory, exist_ok=True)
    
    # Create a subdirectory for CLAHE-enhanced images
    clahe_directory = os.path.join(output_directory, "CLAHE_enhanced")
    os.makedirs(clahe_directory, exist_ok=True)
    
    # Process each image
    for filename in os.listdir(input_directory):
        if filename.startswith("Poly_") and (filename.lower().endswith('.png') or filename.lower().endswith('.jpg')):
            image_path = os.path.join(input_directory, filename)
            
            # Get base name without extension
            base_name = os.path.splitext(filename)[0]
            
            # Define output paths
            clahe_output_path = os.path.join(clahe_directory, f"{base_name}_clahe.png")
            csv_output_path = os.path.join(output_directory, f"{base_name}_gap_analysis.csv")
            new_image_output_path = os.path.join(output_directory, f"{base_name}_gap_visualization.png")
            
            print(f"Processing image: {filename}")
            
            # Step 1: Apply CLAHE enhancement
            enhanced_img = enhance_spot_image(image_path, clahe_output_path)
            if enhanced_img is None:
                continue
            
            # Step 2: Convert to grayscale and analyze pixels
            pil_img = Image.open(clahe_output_path).convert('L')
            gray_img = np.array(pil_img)
            
            gap_data = {}
            height, width = gray_img.shape
            
            # Analyze each pixel
            for row in range(height):
                for col in range(width):
                    is_gap, gray_value = check_gap_conditions(gray_img, row, col)
                    gap_flag = 1 if is_gap else 0
                    gap_data[(row, col)] = (gray_value, gap_flag)
            
            # Step 3: Save CSV with pixel analysis
            save_csv(base_name, gap_data, csv_output_path)
            
            # Step 4: Generate visualization image
            process_new_images(clahe_output_path, gap_data, new_image_output_path)
            
            print(f"Completed processing for: {filename}")

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    process_images(input_directory)
    print("Processed all the images!")
