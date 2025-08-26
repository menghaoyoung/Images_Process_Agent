import os
import csv
import cv2
from PIL import Image
import numpy as np
from collections import defaultdict
import time

# Apply CLAHE enhancement to an image
def enhance_spot_image(image):
    # Create CLAHE object with specified parameters
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(10, 10))
    
    # Apply CLAHE to the image
    enhanced_image = clahe.apply(image)
    
    return enhanced_image

# Check whether the pixel points meet the GAP condition
def check_gap_conditions(gray_image, row, col):
    # Condition 1: Check if the grayscale value is between 1-150 (inclusive)
    if not (1 <= gray_image[row, col] <= 150):
        return False
    
    # Condition 2: Check if at least one adjacent pixel has 20 contiguous pixels meeting the grayscale condition
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    height, width = gray_image.shape
    
    for dr, dc in directions:
        contiguous_count = 0
        r, c = row, col
        
        # Check up to 20 pixels in this direction
        for i in range(20):
            r += dr
            c += dc
            
            # Check if the pixel is within bounds
            if 0 <= r < height and 0 <= c < width:
                # Check if the pixel meets the grayscale condition
                if 1 <= gray_image[r, c] <= 150:
                    contiguous_count += 1
                else:
                    break
            else:
                break
        
        # If we found 20 contiguous pixels, return True
        if contiguous_count >= 20:
            return True
    
    return False

# Process all images in the directory whose filenames start with "Poly_"
def process_images(input_directory):
    # Create output directory if it doesn't exist
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup"
    os.makedirs(output_directory, exist_ok=True)
    
    # Iterate through all files in the input directory
    for filename in os.listdir(input_directory):
        # Check if the file is an image and starts with "Poly_"
        if (filename.startswith("Poly_") and 
            (filename.lower().endswith(".png") or filename.lower().endswith(".jpg"))):
            
            # Full path to the input image
            input_path = os.path.join(input_directory, filename)
            
            # Read the image using OpenCV
            img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
            
            if img is None:
                print(f"Failed to read image: {input_path}")
                continue
            
            # Apply CLAHE enhancement
            enhanced_img = enhance_spot_image(img)
            
            # Save the enhanced image to the output directory
            base_name = os.path.splitext(filename)[0]
            enhanced_path = os.path.join(output_directory, f"{base_name}_enhanced.png")
            cv2.imwrite(enhanced_path, enhanced_img)
            
            # Process the enhanced image and generate CSV and visualization
            process_enhanced_image(enhanced_img, base_name, output_directory)

# Process the enhanced image, generate CSV and visualization
def process_enhanced_image(enhanced_img, base_name, output_directory):
    height, width = enhanced_img.shape
    
    # Convert OpenCV image to PIL Image for easier pixel manipulation
    pil_img = Image.fromarray(enhanced_img)
    
    # Create a new image for visualization
    visualization = Image.new('RGB', (width, height), color=(255, 255, 255))
    
    # Prepare CSV data
    csv_data = []
    
    # Analyze each pixel
    for row in range(height):
        for col in range(width):
            # Get grayscale value
            gray_value = enhanced_img[row, col]
            
            # Check if the pixel meets GAP conditions
            gap_flag = 1 if check_gap_conditions(enhanced_img, row, col) else 0
            
            # Add to CSV data
            csv_data.append([row, col, gray_value, gap_flag])
            
            # Set pixel color in visualization based on GAP flag
            if gap_flag == 1:
                visualization.putpixel((col, row), (0, 0, 0))  # Black for GAP=1
            else:
                visualization.putpixel((col, row), (255, 255, 255))  # White for GAP=0
    
    # Save CSV file
    csv_path = os.path.join(output_directory, f"{base_name}_gap_analysis.csv")
    save_csv(csv_data, csv_path)
    
    # Save visualization image
    visualization_path = os.path.join(output_directory, f"{base_name}_gap_visualization.png")
    visualization.save(visualization_path)

# Save pixel analysis data to CSV
def save_csv(data, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['Row', 'Column', 'Grayscale_Value', 'GAP_Flag'])
        # Write data
        writer.writerows(data)

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    process_images(input_directory)
    print("Processed all the images!")
