import os
import csv
import cv2
from PIL import Image
import numpy as np
from collections import defaultdict
import time

def enhance_spot_image(image_path, output_path):
    """Apply CLAHE enhancement to an image."""
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error reading image: {image_path}")
        return None
    
    # Convert to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Split the LAB image into L, A, and B channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to the L channel
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(10, 10))
    cl = clahe.apply(l)
    
    # Merge the CLAHE enhanced L channel with the original A and B channels
    merged = cv2.merge((cl, a, b))
    
    # Convert back to BGR color space
    enhanced_img = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
    
    # Save the enhanced image
    cv2.imwrite(output_path, enhanced_img)
    
    return output_path

def check_gap_conditions(gray_img, row, col):
    """
    Check if a pixel meets the GAP conditions:
    1. Grayscale value between 1-150 (inclusive)
    2. At least one adjacent pixel (up/down/left/right) has 25 contiguous pixels 
       meeting the grayscale condition
    """
    height, width = gray_img.shape
    
    # Check first condition: grayscale value between 1-150
    pixel_value = gray_img[row, col]
    if not (1 <= pixel_value <= 150):
        return 0
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Check second condition
    for dr, dc in directions:
        r, c = row + dr, col + dc
        
        # Skip if out of bounds
        if not (0 <= r < height and 0 <= c < width):
            continue
        
        # Check if adjacent pixel has 25 contiguous pixels meeting the condition
        contiguous_count = 0
        visited = set()
        queue = [(r, c)]
        
        while queue and contiguous_count < 25:
            curr_r, curr_c = queue.pop(0)
            
            # Skip if already visited or out of bounds
            if (curr_r, curr_c) in visited or not (0 <= curr_r < height and 0 <= curr_c < width):
                continue
            
            visited.add((curr_r, curr_c))
            
            # Check if the pixel meets the grayscale condition
            if 1 <= gray_img[curr_r, curr_c] <= 150:
                contiguous_count += 1
                
                # Add adjacent pixels to the queue
                for adj_dr, adj_dc in directions:
                    new_r, new_c = curr_r + adj_dr, curr_c + adj_dc
                    if (new_r, new_c) not in visited and 0 <= new_r < height and 0 <= new_c < width:
                        queue.append((new_r, new_c))
        
        if contiguous_count >= 25:
            return 1
    
    return 0

def process_images(input_directory):
    """Process all images in the directory whose filenames start with 'Poly_'"""
    # Create output directories if they don't exist
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup6"
    clahe_directory = os.path.join(output_directory, "CLAHE_enhanced")
    csv_directory = os.path.join(output_directory, "CSV_files")
    gap_images_directory = os.path.join(output_directory, "GAP_images")
    
    for directory in [output_directory, clahe_directory, csv_directory, gap_images_directory]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Get all image files starting with "Poly_"
    image_files = [f for f in os.listdir(input_directory) 
                  if f.startswith("Poly_") and (f.lower().endswith('.png') or f.lower().endswith('.jpg'))]
    
    print(f"Found {len(image_files)} images to process")
    
    for image_file in image_files:
        print(f"Processing {image_file}...")
        image_path = os.path.join(input_directory, image_file)
        
        # Get the base name without extension
        base_name = os.path.splitext(image_file)[0]
        
        # Apply CLAHE enhancement
        clahe_output_path = os.path.join(clahe_directory, f"{base_name}_clahe.png")
        enhanced_image_path = enhance_spot_image(image_path, clahe_output_path)
        
        if enhanced_image_path:
            # Process the enhanced image
            process_enhanced_image(enhanced_image_path, base_name, csv_directory, gap_images_directory)

def process_enhanced_image(image_path, base_name, csv_directory, gap_images_directory):
    """Process a CLAHE-enhanced image to identify GAP pixels and generate outputs"""
    # Open the image with PIL
    pil_img = Image.open(image_path).convert('L')  # Convert to grayscale
    width, height = pil_img.size
    
    # Convert to numpy array for faster processing
    gray_img = np.array(pil_img)
    
    # Create a new image to highlight GAP pixels
    gap_image = Image.new('RGB', (width, height), color=(255, 255, 255))
    gap_pixels = gap_image.load()
    
    # Prepare CSV data
    csv_data = []
    
    print(f"Analyzing pixels for {base_name}...")
    
    # Process each pixel
    for row in range(height):
        for col in range(width):
            gray_value = gray_img[row, col]
            gap_flag = check_gap_conditions(gray_img, row, col)
            
            # Add to CSV data
            csv_data.append((row, col, int(gray_value), gap_flag))
            
            # Set pixel color in gap image
            if gap_flag == 1:
                gap_pixels[col, row] = (0, 0, 0)  # Black for GAP=1
    
    # Save CSV file
    csv_path = os.path.join(csv_directory, f"{base_name}_gap_analysis.csv")
    save_csv(csv_path, csv_data)
    
    # Save GAP image
    gap_image_path = os.path.join(gap_images_directory, f"{base_name}_gap.png")
    gap_image.save(gap_image_path)
    
    print(f"Completed analysis for {base_name}")

def save_csv(csv_path, data):
    """Save pixel analysis data to a CSV file"""
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Row', 'Column', 'Grayscale_Value', 'GAP_Flag'])
        writer.writerows(data)

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    process_images(input_directory)
    print("Processed all the images!")
