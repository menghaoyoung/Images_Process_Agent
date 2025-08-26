import os
import csv
import cv2
from PIL import Image
import numpy as np
from collections import defaultdict
import time

# Enhance image using CLAHE
def enhance_spot_image(image_path, output_path):
    # Read the image using cv2
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not read image: {image_path}")
        return None
    
    # Convert to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Split the LAB image into L, A, and B channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to the L channel
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(10, 10))
    cl = clahe.apply(l)
    
    # Merge the CLAHE enhanced L channel with the original A and B channels
    limg = cv2.merge((cl, a, b))
    
    # Convert back to BGR color space
    enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    # Save the enhanced image
    cv2.imwrite(output_path, enhanced)
    
    return enhanced

# Check whether the pixel points meet the GAP condition
def check_gap_conditions(gray_img, row, col):
    height, width = gray_img.shape
    
    # Check if grayscale value is between 1-155
    if not (1 <= gray_img[row, col] <= 155):
        return False
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        # Check if we can go 25 steps in this direction
        contiguous_count = 0
        for step in range(1, 26):
            r, c = row + dr * step, col + dc * step
            
            # Check if the position is valid
            if 0 <= r < height and 0 <= c < width:
                if 1 <= gray_img[r, c] <= 155:
                    contiguous_count += 1
                else:
                    break
            else:
                break
        
        # If we found 25 contiguous pixels meeting the condition
        if contiguous_count >= 25:
            return True
    
    return False

# Process all images in the directory whose filenames start with "Poly_"
def process_images(input_directory):
    # Create output directory if it doesn't exist
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup3"
    os.makedirs(output_directory, exist_ok=True)
    
    # Get all image files with "Poly_" prefix
    image_files = [f for f in os.listdir(input_directory) 
                  if f.startswith("Poly_") and 
                  (f.lower().endswith('.png') or f.lower().endswith('.jpg'))]
    
    for image_file in image_files:
        print(f"Processing {image_file}...")
        
        # Full paths
        input_path = os.path.join(input_directory, image_file)
        
        # Get the base name without extension
        base_name = os.path.splitext(image_file)[0]
        
        # Create enhanced image path
        enhanced_path = os.path.join(output_directory, f"{base_name}_enhanced.png")
        
        # Create output CSV path
        csv_path = os.path.join(output_directory, f"{base_name}_gap_analysis.csv")
        
        # Create output image path
        output_image_path = os.path.join(output_directory, f"{base_name}_gap_result.png")
        
        # Enhance the image using CLAHE
        enhance_spot_image(input_path, enhanced_path)
        
        # Open the enhanced image with PIL
        img = Image.open(enhanced_path).convert('L')
        
        # Convert to numpy array for processing
        gray_img = np.array(img)
        
        # Create a list to store pixel data
        pixel_data = []
        
        # Create a new image to highlight GAP pixels
        gap_image = np.ones_like(gray_img) * 255  # Start with all white
        
        height, width = gray_img.shape
        
        # Process each pixel
        for row in range(height):
            for col in range(width):
                gray_value = int(gray_img[row, col])
                
                # Check GAP conditions
                is_gap = check_gap_conditions(gray_img, row, col)
                
                # Store pixel data
                pixel_data.append([row, col, gray_value, 1 if is_gap else 0])
                
                # Mark GAP pixels in the output image
                if is_gap:
                    gap_image[row, col] = 0  # Black
        
        # Save the CSV file
        save_csv(csv_path, pixel_data)
        
        # Save the output image
        cv2.imwrite(output_image_path, gap_image)

# Stores all pixel analysis data, naming: {original_image_name}_gap_analysis.csv
def save_csv(csv_path, pixel_data):
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Row', 'Column', 'Grayscale Value', 'GAP Flag'])
        writer.writerows(pixel_data)

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    process_images(input_directory)
    print("Processed all the images!")
