import os
import csv
import cv2
from PIL import Image
import numpy as np
from collections import defaultdict
import time

# Enhance image using CLAHE
def enhance_spot_image(image_path, output_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image {image_path}")
        return None
    
    # Convert to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Split the LAB image to L, A and B channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(10, 10))
    cl = clahe.apply(l)
    
    # Merge the CLAHE enhanced L channel with the original A and B channels
    merged = cv2.merge((cl, a, b))
    
    # Convert back to BGR color space
    enhanced_img = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
    
    # Save the enhanced image
    cv2.imwrite(output_path, enhanced_img)
    
    return enhanced_img

# Check whether the pixel points meet the GAP condition
def check_gap_conditions(gray_img, row, col):
    height, width = gray_img.shape
    pixel_value = gray_img[row, col]
    
    # Check first condition: grayscale value between 1-150 (inclusive)
    if not (1 <= pixel_value <= 150):
        return False
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        # Check if there are 25 contiguous pixels in this direction meeting the grayscale condition
        contiguous_count = 0
        for i in range(1, 26):  # Check 25 pixels
            new_row, new_col = row + dr * i, col + dc * i
            
            # Check if the new position is within bounds
            if 0 <= new_row < height and 0 <= new_col < width:
                if 1 <= gray_img[new_row, new_col] <= 150:
                    contiguous_count += 1
                else:
                    break
            else:
                break
        
        if contiguous_count >= 25:
            return True
    
    return False

# Process all images in the directory whose filenames start with "Poly_"
def process_images(input_directory):
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup9"
    os.makedirs(output_directory, exist_ok=True)
    
    # Get all image files with "Poly_" prefix
    image_files = [f for f in os.listdir(input_directory) 
                  if f.startswith("Poly_") and (f.lower().endswith(".png") or f.lower().endswith(".jpg"))]
    
    for image_file in image_files:
        print(f"Processing {image_file}...")
        image_path = os.path.join(input_directory, image_file)
        
        # Create enhanced image filename
        base_name = os.path.splitext(image_file)[0]
        enhanced_image_path = os.path.join(output_directory, f"{base_name}_enhanced.png")
        
        # Enhance the image using CLAHE
        enhanced_img = enhance_spot_image(image_path, enhanced_image_path)
        if enhanced_img is None:
            continue
        
        # Convert to grayscale using PIL
        pil_img = Image.open(enhanced_image_path).convert('L')
        gray_img = np.array(pil_img)
        
        # Process the grayscale image to identify GAP pixels
        process_grayscale_image(gray_img, base_name, output_directory)

# Process grayscale image to identify GAP pixels
def process_grayscale_image(gray_img, base_name, output_directory):
    height, width = gray_img.shape
    results = []
    
    # Create a new image to highlight GAP pixels
    highlight_img = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background
    
    # Process each pixel
    for row in range(height):
        for col in range(width):
            pixel_value = gray_img[row, col]
            is_gap = check_gap_conditions(gray_img, row, col)
            
            # Store the result
            results.append((row, col, pixel_value, 1 if is_gap else 0))
            
            # Highlight GAP pixels in black
            if is_gap:
                highlight_img[row, col] = [0, 0, 0]  # Black
    
    # Save the CSV file
    csv_path = os.path.join(output_directory, f"{base_name}_gap_analysis.csv")
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Row', 'Column', 'Grayscale Value', 'GAP Flag'])
        writer.writerows(results)
    
    # Save the highlighted image
    highlight_path = os.path.join(output_directory, f"{base_name}_gap_highlighted.png")
    cv2.imwrite(highlight_path, highlight_img)

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    process_images(input_directory)
    print("Processed all the images!")
