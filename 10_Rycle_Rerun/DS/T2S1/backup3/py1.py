import os
import numpy as np
from PIL import Image
import argparse
import sys

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Bresenham's line algorithm to get integer coordinates along a line segment
def bresenham_line(x0, y0, x1, y1):
    """Generate integer coordinates for all pixels along a straight line from (x0,y0) to (x1,y1)."""
    points = []
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy  # Initial error value
    
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:  # Step in x-direction
            err += dy
            x0 += sx
        if e2 <= dx:  # Step in y-direction
            err += dx
            y0 += sy
    return points

def main():
    # Parse command-line argument for resolution
    parser = argparse.ArgumentParser(description='Process line segments in an image.')
    parser.add_argument('-resolution', type=float, required=True, help='Resolution value (e.g., 1.08)')
    args = parser.parse_args()
    resolution = args.resolution

    # Fixed parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup3"
    start_point = (152, 29)
    end_point = (136, 91)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Load and convert image to grayscale
    try:
        img = Image.open(image_path).convert('L')
        img_arr = np.array(img)
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # Extract line coordinates using Bresenham's algorithm
    x0, y0 = start_point
    x1, y1 = end_point
    line_points = bresenham_line(x0, y0, x1, y1)
    
    # Collect grayscale values with bounds checking
    grayscale_values = []
    for (x, y) in line_points:
        if 0 <= y < img_arr.shape[0] and 0 <= x < img_arr.shape[1]:
            grayscale_values.append(int(img_arr[y, x]))
        else:
            grayscale_values.append(0)  # Out-of-bound points set to 0
    
    # Calculate physical length of the line segment
    pixel_length = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    physical_length = pixel_length * resolution
    print(f"Physical length: {physical_length:.2f} units")
    
    # Save grayscale values to CSV
    filename = f"grayscale_values_res_{resolution:.2f}.csv"
    output_path = os.path.join(output_dir, filename)
    np.savetxt(output_path, grayscale_values, delimiter=',', fmt='%d')
    print(f"Saved grayscale values to: {output_path}")

if __name__ == '__main__':
    main()
