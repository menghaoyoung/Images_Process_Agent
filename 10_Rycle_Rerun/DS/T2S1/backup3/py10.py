import os
import sys
import numpy as np
from PIL import Image
import math
import argparse

def main():
    # Fixed parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup3"
    start_point = (152, 29)
    end_point = (136, 91)
    
    # Parse command line argument
    parser = argparse.ArgumentParser()
    parser.add_argument('-resolution', type=float, required=True)
    args = parser.parse_args()
    resolution = args.resolution

    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Load and process image
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
        
        # Calculate coordinates using Bresenham's algorithm
        x0, y0 = start_point
        x1, y1 = end_point
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        
        line_points = []
        while True:
            line_points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
        
        # Extract grayscale values with boundary checking
        grayscale_values = []
        for x, y in line_points:
            if 0 <= y < img_array.shape[0] and 0 <= x < img_array.shape[1]:
                grayscale_values.append(img_array[y, x])
            else:
                grayscale_values.append(0)
        
        # Calculate physical length
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        pixel_length = math.sqrt(dx**2 + dy**2)
        physical_length = pixel_length * resolution
        print(f"Physical line length: {physical_length:.4f} units")
        
        # Save to CSV with consistent filename format
        csv_filename = f"grayscale_values_{resolution:.2f}.csv"
        csv_path = os.path.join(output_dir, csv_filename)
        np.savetxt(csv_path, grayscale_values, fmt='%d', delimiter=',')
        print(f"Saved grayscale values to: {csv_path}")
        
        # Immediate verification
        if os.path.exists(csv_path):
            file_size = os.path.getsize(csv_path)
            print(f"Verification: CSV created ({file_size} bytes)")
            print("Calculation successful")
        else:
            print("Error: CSV file not created")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
