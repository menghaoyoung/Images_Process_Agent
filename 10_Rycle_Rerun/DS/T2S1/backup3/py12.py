import os
import numpy as np
from PIL import Image
import math
import sys
import time

# Fixed parameters
IMAGE_PATH = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
OUTPUT_DIR = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup3"
START_POINT = (152, 29)
END_POINT = (136, 91)
RESOLUTION = 1.08  # Fixed resolution as per task

def calculate_line_points(start, end):
    """Bresenham's line algorithm to get coordinates between two points"""
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    
    points = []
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
    return points

def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # CSV file path with consistent naming
    csv_filename = f"grayscale_values_{RESOLUTION:.2f}.csv"
    csv_path = os.path.join(OUTPUT_DIR, csv_filename)
    
    print(f"Processing image: {IMAGE_PATH}")
    print(f"Output CSV: {csv_path}")
    print(f"Resolution: {RESOLUTION}")
    
    try:
        # Load and process image
        img = Image.open(IMAGE_PATH).convert('L')
        img_array = np.array(img)
        print("Image loaded successfully")
        
        # Get line coordinates
        line_points = calculate_line_points(START_POINT, END_POINT)
        print(f"Line segment contains {len(line_points)} points")
        
        # Extract grayscale values
        grayscale_values = []
        for x, y in line_points:
            if 0 <= y < img_array.shape[0] and 0 <= x < img_array.shape[1]:
                grayscale_values.append(img_array[y, x])
            else:
                grayscale_values.append(0)
        print("Grayscale values extracted")
        
        # Calculate physical length
        dx = END_POINT[0] - START_POINT[0]
        dy = END_POINT[1] - START_POINT[1]
        pixel_length = math.sqrt(dx**2 + dy**2)
        physical_length = pixel_length * RESOLUTION
        print(f"Physical line length: {physical_length:.4f} units")
        
        # Save to CSV
        np.savetxt(csv_path, grayscale_values, fmt='%d', delimiter=',')
        print("CSV file saved successfully")
        
        # Verify CSV creation
        print("\nVerifying CSV file...")
        time.sleep(1)  # Allow filesystem to update
        
        if os.path.exists(csv_path):
            file_size = os.path.getsize(csv_path)
            if file_size > 0:
                print(f"Verification: CSV exists ({file_size} bytes)")
                print("Calculation successful")
                return
            print("Error: CSV file is empty")
        else:
            print("Error: CSV file not found")
        
        print("Calculation failed")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Calculation failed")

if __name__ == '__main__':
    main()
