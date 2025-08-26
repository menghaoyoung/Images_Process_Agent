import os
import csv
import cv2
from PIL import Image
import numpy as np
from collections import defaultdict
import time

def enhance_spot_image(image):
    """Apply CLAHE enhancement to the input image"""
    # Convert to grayscale if it's a color image
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Apply CLAHE
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(10, 10))
    enhanced = clahe.apply(gray)
    
    return enhanced

def check_gap_conditions(gray_img, row, col):
    """
    Check whether the pixel points meet the GAP condition:
    (1) Grayscale value between 1–160 (inclusive)
    (2) At least one adjacent pixel (up/down/left/right) has 25 contiguous pixels meeting the grayscale condition.
    """
    height, width = gray_img.shape
    
    # Check condition 1: Grayscale value between 1-160
    pixel_value = gray_img[row, col]
    if not (1 <= pixel_value <= 160):
        return False, pixel_value
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Check condition 2: At least one adjacent pixel has 25 contiguous pixels meeting grayscale condition
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        
        # Skip if out of bounds
        if not (0 <= nr < height and 0 <= nc < width):
            continue
        
        # Check if adjacent pixel is within grayscale range
        if not (1 <= gray_img[nr, nc] <= 160):
            continue
        
        # Check for 25 contiguous pixels
        count = 1  # Start with 1 for the adjacent pixel
        visited = set([(nr, nc)])
        queue = [(nr, nc)]
        
        while queue and count < 25:
            r, c = queue.pop(0)
            
            for dr2, dc2 in directions:
                nr2, nc2 = r + dr2, c + dc2
                
                # Skip if out of bounds or already visited
                if not (0 <= nr2 < height and 0 <= nc2 < width) or (nr2, nc2) in visited:
                    continue
                
                # If pixel meets grayscale condition, add to count and queue
                if 1 <= gray_img[nr2, nc2] <= 160:
                    count += 1
                    visited.add((nr2, nc2))
                    queue.append((nr2, nc2))
                    
                    # Early exit if we found 25 contiguous pixels
                    if count >= 25:
                        return True, pixel_value
        
    return False, pixel_value

def process_images(input_directory):
    """Process all images in the directory whose filenames start with 'Poly_'"""
    # Create output directory if it doesn't exist
    output_directory = os.path.join(os.path.dirname(input_directory), "ALL_RESULT", "CLAUDE", "T3", "backup1")
    os.makedirs(output_directory, exist_ok=True)
    
    # Get all image files with 'Poly_' prefix
    image_files = [f for f in os.listdir(input_directory) 
                  if f.startswith('Poly_') and (f.lower().endswith('.png') or f.lower().endswith('.jpg'))]
    
    print(f"Found {len(image_files)} images to process.")
    
    for image_file in image_files:
        print(f"Processing {image_file}...")
        input_path = os.path.join(input_directory, image_file)
        
        # Read the image and apply CLAHE enhancement
        original_img = cv2.imread(input_path)
        if original_img is None:
            print(f"Error: Could not read image {input_path}")
            continue
        
        # Apply CLAHE enhancement
        enhanced_img = enhance_spot_image(original_img)
        
        # Save the enhanced image
        enhanced_filename = f"enhanced_{image_file}"
        enhanced_path = os.path.join(output_directory, enhanced_filename)
        cv2.imwrite(enhanced_path, enhanced_img)
        
        # Convert to PIL Image for processing
        pil_img = Image.fromarray(enhanced_img)
        
        # Process the image and get GAP analysis
        original_name = os.path.splitext(image_file)[0]
        gap_data = analyze_gap_pixels(enhanced_img, original_name)
        
        # Save results
        csv_filename = f"{original_name}_gap_analysis.csv"
        csv_path = os.path.join(output_directory, csv_filename)
        save_csv(gap_data, csv_path)
        
        # Generate the new image highlighting GAP pixels
        new_image_path = os.path.join(output_directory, f"{original_name}_gap_highlighted.png")
        process_new_image(gap_data, enhanced_img.shape, new_image_path)

def analyze_gap_pixels(gray_img, image_name):
    """Analyze all pixels in the image for GAP conditions"""
    height, width = gray_img.shape
    gap_data = []
    
    print(f"Analyzing {image_name} for GAP pixels ({height}x{width})...")
    start_time = time.time()
    
    for row in range(height):
        if row % 100 == 0:  # Progress update
            elapsed = time.time() - start_time
            print(f"Processing row {row}/{height} ({row/height*100:.1f}%) - Elapsed: {elapsed:.2f}s")
        
        for col in range(width):
            is_gap, pixel_value = check_gap_conditions(gray_img, row, col)
            gap_flag = 1 if is_gap else 0
            gap_data.append((row, col, pixel_value, gap_flag))
    
    print(f"Analysis complete for {image_name} - Total time: {time.time() - start_time:.2f}s")
    return gap_data

def process_new_image(gap_data, img_shape, output_path):
    """
    Generate a new PNG image highlighting points with GAP flag = 1 in black (RGB: 0, 0, 0),
    and points with GAP flag = 0 in white (RGB: 255, 255, 255).
    """
    height, width = img_shape
    new_image = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background
    
    for row, col, _, gap_flag in gap_data:
        if gap_flag == 1:
            new_image[row, col] = [0, 0, 0]  # Black for GAP pixels
    
    cv2.imwrite(output_path, new_image)
    print(f"Created highlighted image: {output_path}")

def save_csv(gap_data, output_path):
    """
    Save pixel analysis data to CSV with columns:
    Coordinates (row, column), Grayscale value, GAP flag (0 or 1)
    """
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Row', 'Column', 'Grayscale_Value', 'GAP_Flag'])
        writer.writerows(gap_data)
    
    print(f"Saved CSV: {output_path}")

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    process_images(input_directory)
    print("Processed all the images!")
