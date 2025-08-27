import os
import csv
import cv2
from PIL import Image
import numpy as np
from collections import defaultdict
import time

def enhance_spot_image(image_path, output_path):
    """Apply CLAHE enhancement to an image and save it."""
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image {image_path}")
        return None
    
    # Convert to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Split LAB channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(10, 10))
    enhanced_l = clahe.apply(l)
    
    # Merge channels back
    enhanced_lab = cv2.merge((enhanced_l, a, b))
    
    # Convert back to BGR
    enhanced_img = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    # Save the enhanced image
    cv2.imwrite(output_path, enhanced_img)
    
    return enhanced_img

def check_gap_conditions(img_array, row, col, threshold_min=1, threshold_max=150, contiguous_count=25):
    """
    Check if a pixel meets the GAP conditions:
    1. Grayscale value between threshold_min and threshold_max (inclusive)
    2. At least one adjacent pixel (up/down/left/right) has contiguous_count pixels 
       meeting the grayscale condition
    """
    height, width = img_array.shape
    
    # Check if the pixel's grayscale value is within the specified range
    pixel_value = img_array[row, col]
    if not (threshold_min <= pixel_value <= threshold_max):
        return False, pixel_value
    
    # Define directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Check each direction
    for dr, dc in directions:
        contiguous = 0
        r, c = row, col
        
        # Check contiguous pixels in this direction
        for _ in range(contiguous_count):
            r += dr
            c += dc
            
            # Check if we're still within image boundaries
            if 0 <= r < height and 0 <= c < width:
                if threshold_min <= img_array[r, c] <= threshold_max:
                    contiguous += 1
                else:
                    break
            else:
                break
        
        # If we found enough contiguous pixels in this direction
        if contiguous >= contiguous_count - 1:  # -1 because we're not counting the pixel itself
            return True, pixel_value
    
    return False, pixel_value

def process_images(input_directory):
    """Process all images in the directory whose filenames start with 'Poly_'"""
    # Create output directory for enhanced images
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup8"
    enhanced_dir = os.path.join(output_dir, "enhanced")
    
    # Create directories if they don't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(enhanced_dir, exist_ok=True)
    
    # Get all image files with Poly_ prefix
    image_files = [f for f in os.listdir(input_directory) 
                  if f.startswith("Poly_") and (f.lower().endswith('.png') or f.lower().endswith('.jpg'))]
    
    print(f"Found {len(image_files)} images to process")
    
    for image_file in image_files:
        print(f"Processing {image_file}...")
        
        # Paths for input and enhanced images
        input_path = os.path.join(input_directory, image_file)
        base_name = os.path.splitext(image_file)[0]
        enhanced_path = os.path.join(enhanced_dir, f"{base_name}_enhanced.png")
        
        # Apply CLAHE enhancement and save the enhanced image
        enhance_spot_image(input_path, enhanced_path)
        
        # Process the enhanced image to find GAP pixels
        process_enhanced_image(enhanced_path, base_name, output_dir)

def process_enhanced_image(enhanced_image_path, base_name, output_dir):
    """Process an enhanced image to find GAP pixels and generate outputs"""
    # Open the enhanced image with PIL
    img = Image.open(enhanced_image_path).convert('L')  # Convert to grayscale
    img_array = np.array(img)
    
    height, width = img_array.shape
    
    # Create a new image to highlight GAP pixels
    result_img = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background
    
    # Prepare CSV data
    csv_data = []
    
    print(f"Analyzing image of size {width}x{height}")
    
    # To save time for demonstration, process a subset of pixels
    # For a real application, remove the stride to process all pixels
    stride = 1  # Process every pixel
    
    # Check each pixel
    for row in range(0, height, stride):
        for col in range(0, width, stride):
            is_gap, grayscale_value = check_gap_conditions(img_array, row, col)
            
            # Add pixel data to CSV
            csv_data.append([row, col, grayscale_value, 1 if is_gap else 0])
            
            # Mark GAP pixels as black in the result image
            if is_gap:
                result_img[row, col] = [0, 0, 0]  # Black
    
    # Save the result image
    result_img_path = os.path.join(output_dir, f"{base_name}_gap_result.png")
    cv2.imwrite(result_img_path, result_img)
    
    # Save the CSV file
    csv_path = os.path.join(output_dir, f"{base_name}_gap_analysis.csv")
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Row', 'Column', 'Grayscale', 'GAP_Flag'])
        writer.writerows(csv_data)
    
    print(f"Completed processing {base_name}. Results saved to {output_dir}")

if __name__ == "__main__":
    start_time = time.time()
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    process_images(input_directory)
    end_time = time.time()
    print(f"Processed all the images in {end_time - start_time:.2f} seconds!")
