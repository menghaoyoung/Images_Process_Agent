import os
import csv
import cv2
from PIL import Image
import numpy as np
from collections import defaultdict
import time

def enhance_spot_image(image_path, output_path):
    """
    Enhance an image using CLAHE
    """
    # Read the image using cv2
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error reading image {image_path}")
        return None
    
    # Convert to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Split the LAB channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to the L channel
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(10, 10))
    enhanced_l = clahe.apply(l)
    
    # Merge the enhanced L channel with the original A and B channels
    enhanced_lab = cv2.merge((enhanced_l, a, b))
    
    # Convert back to BGR color space
    enhanced_img = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    # Save the enhanced image
    cv2.imwrite(output_path, enhanced_img)
    
    return output_path

def check_gap_conditions(gray_img, row, col, threshold_min=1, threshold_max=150, required_contiguous=25):
    """
    Check if a pixel meets the GAP conditions:
    1. Grayscale value between threshold_min and threshold_max (inclusive)
    2. At least one adjacent pixel (up/down/left/right) has required_contiguous contiguous pixels 
       meeting the grayscale condition
    """
    height, width = gray_img.shape
    
    # Check if the pixel's grayscale value is within the threshold
    pixel_value = gray_img[row, col]
    if not (threshold_min <= pixel_value <= threshold_max):
        return False
    
    # Define directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Check each direction
    for dr, dc in directions:
        contiguous_count = 0
        r, c = row, col
        
        # Count contiguous pixels in this direction
        while 0 <= r < height and 0 <= c < width and contiguous_count < required_contiguous:
            r += dr
            c += dc
            
            # If out of bounds, break
            if not (0 <= r < height and 0 <= c < width):
                break
                
            # If pixel value is within threshold, increment count
            if threshold_min <= gray_img[r, c] <= threshold_max:
                contiguous_count += 1
            else:
                break
        
        # If we found enough contiguous pixels in this direction
        if contiguous_count >= required_contiguous:
            return True
    
    return False

def process_images(input_directory):
    """
    Process all images in the directory whose filenames start with "Poly_"
    """
    # Create output directory for enhanced images
    enhanced_dir = os.path.join(os.path.dirname(input_directory), "ALL_RESULT", "CLAUDE", "T3", "backup7", "enhanced")
    os.makedirs(enhanced_dir, exist_ok=True)
    
    # Create output directory for GAP analysis results
    output_dir = os.path.join(os.path.dirname(input_directory), "ALL_RESULT", "CLAUDE", "T3", "backup7")
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all image files starting with "Poly_"
    image_files = [f for f in os.listdir(input_directory) 
                  if f.startswith("Poly_") and (f.lower().endswith('.png') or f.lower().endswith('.jpg'))]
    
    for image_file in image_files:
        print(f"Processing {image_file}...")
        
        # Enhance the image using CLAHE
        input_path = os.path.join(input_directory, image_file)
        enhanced_filename = f"enhanced_{image_file}"
        enhanced_path = os.path.join(enhanced_dir, enhanced_filename)
        
        enhanced_path = enhance_spot_image(input_path, enhanced_path)
        if enhanced_path is None:
            continue
        
        # Process the enhanced image
        process_enhanced_image(enhanced_path, image_file, output_dir)

def process_enhanced_image(enhanced_image_path, original_filename, output_dir):
    """
    Process an enhanced image to detect GAP pixels and generate outputs
    """
    # Open the enhanced image with PIL
    pil_img = Image.open(enhanced_image_path)
    gray_img = pil_img.convert('L')
    
    # Convert to numpy array for faster processing
    gray_array = np.array(gray_img)
    
    height, width = gray_array.shape
    
    # Prepare CSV data
    csv_data = []
    
    # Prepare a new image to highlight GAP pixels
    gap_highlight = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Process each pixel
    for row in range(height):
        for col in range(width):
            pixel_value = gray_array[row, col]
            
            # Check if pixel meets GAP conditions
            is_gap = check_gap_conditions(gray_array, row, col)
            
            # Add to CSV data
            csv_data.append((row, col, int(pixel_value), 1 if is_gap else 0))
            
            # Update highlight image
            if is_gap:
                gap_highlight[row, col] = [0, 0, 0]  # Black for GAP pixels
    
    # Save CSV file
    base_name = os.path.splitext(original_filename)[0]
    csv_path = os.path.join(output_dir, f"{base_name}_gap_analysis.csv")
    
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Row', 'Column', 'Grayscale_Value', 'GAP_Flag'])
        writer.writerows(csv_data)
    
    # Save highlight image
    highlight_path = os.path.join(output_dir, f"{base_name}_gap_highlight.png")
    cv2.imwrite(highlight_path, gap_highlight)

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    start_time = time.time()
    process_images(input_directory)
    end_time = time.time()
    print(f"Processed all the images! Time taken: {end_time - start_time:.2f} seconds")
