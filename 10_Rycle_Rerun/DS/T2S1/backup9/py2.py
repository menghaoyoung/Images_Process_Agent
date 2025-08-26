import os
import numpy as np
from PIL import Image
import sys
import argparse
import math
import csv

def bresenham_line(x0, y0, x1, y1):
    """Generate line coordinates using Bresenham's algorithm"""
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return points

def get_line_grayscale(img_array, start_point, end_point):
    """Extract grayscale values along a line segment"""
    x0, y0 = start_point
    x1, y1 = end_point
    line_points = bresenham_line(x0, y0, x1, y1)
    return [img_array[y, x] for (x, y) in line_points]

def validate_points(img_width, img_height, start_point, end_point):
    """Validate start and end points are within image bounds"""
    x1, y1 = start_point
    x2, y2 = end_point
    if not (0 <= x1 < img_width and 0 <= y1 < img_height):
        raise ValueError(f"Start point {start_point} is out of image bounds")
    if not (0 <= x2 < img_width and 0 <= y2 < img_height):
        raise ValueError(f"End point {end_point} is out of image bounds")

def main():
    parser = argparse.ArgumentParser(description='Extract grayscale values along a line segment')
    parser.add_argument('-resolution', type=float, required=True, 
                        help='Resolution value (e.g., 1.08) for physical length calculation')
    args = parser.parse_args()
    
    # Fixed parameters from the task
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup9"
    
    try:
        # Validate and process image
        img = Image.open(image_path)
        if img.mode != 'L':
            img = img.convert('L')
        img_array = np.array(img)
        img_height, img_width = img_array.shape
        
        # Validate coordinates
        validate_points(img_width, img_height, start_point, end_point)
        
        # Calculate physical length
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        pixel_length = math.sqrt(dx**2 + dy**2)
        physical_length = pixel_length * args.resolution
        print(f"Physical length: {physical_length:.2f} units")
        
        # Get grayscale values and save to CSV
        grayscale_values = get_line_grayscale(img_array, start_point, end_point)
        os.makedirs(output_dir, exist_ok=True)
        output_csv = os.path.join(output_dir, f"grayscale_values_res_{args.resolution:.2f}.csv")
        
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Index', 'Grayscale_Value'])
            for i, value in enumerate(grayscale_values):
                writer.writerow([i, value])
        
        print(f"Saved {len(grayscale_values)} values to {output_csv}")
        print("Calculation successful")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
