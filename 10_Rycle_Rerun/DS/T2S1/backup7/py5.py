import os
import numpy as np
import argparse
from PIL import Image
import math
import sys

def bresenham(x0, y0, x1, y1):
    """Generate integer coordinates between two points using Bresenham's algorithm"""
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

def main():
    # Setup argument parser with required resolution parameter
    parser = argparse.ArgumentParser(description='Calculate line segment grayscale values')
    parser.add_argument('-resolution', required=True, type=float, 
                        help='Resolution value (e.g., 1.08)')
    
    # Parse arguments
    args = parser.parse_args()
    resolution = args.resolution
    
    # Fixed parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup7"
    
    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Load and convert image to grayscale
        image = Image.open(image_path).convert('L')
    except Exception as e:
        print(f"Error loading image: {e}")
        sys.exit(1)
    
    # Calculate physical length of segment
    dx = start_point[0] - end_point[0]
    dy = start_point[1] - end_point[1]
    distance_pixels = math.sqrt(dx**2 + dy**2)
    physical_length = distance_pixels * resolution
    print(f"Physical length of the segment: {physical_length:.2f} units")
    
    # Get all points along the line using Bresenham's algorithm
    line_points = bresenham(start_point[0], start_point[1], 
                            end_point[0], end_point[1])
    
    # Extract grayscale values along the line
    grayscale_values = []
    for x, y in line_points:
        try:
            grayscale_values.append(image.getpixel((x, y)))
        except IndexError:
            print(f"Warning: Point ({x}, {y}) is out of image bounds")
            grayscale_values.append(0)
    
    # Save to CSV file
    csv_filename = f"grayscale_values_res_{resolution}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    np.savetxt(csv_path, grayscale_values, fmt='%d', delimiter=',')
    print(f"Saved {len(grayscale_values)} grayscale values to {csv_path}")

if __name__ == '__main__':
    main()
