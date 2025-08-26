import os
import numpy as np
import sys
import io
import math
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Bresenham's line algorithm to get pixel coordinates
def bresenham(x0, y0, x1, y1):
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

# Get grayscale values along a line segment
def get_line_grayscale(img_array, start, end):
    x0, y0 = start
    x1, y1 = end
    pixels = bresenham(x0, y0, x1, y1)
    gray_values = []
    rows, cols = img_array.shape
    
    for x, y in pixels:
        if 0 <= y < rows and 0 <= x < cols:
            gray_values.append(img_array[y, x])
        else:
            gray_values.append(0)  # Handle out-of-bound points
    return gray_values

def main():
    # Default parameters
    base_img_dir = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS"
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup4"
    start_point = (152, 29)
    end_point = (136, 91)
    
    # Parse command-line argument for resolution
    resolution = None
    for arg in sys.argv[1:]:
        if arg.startswith('-resolution='):
            try:
                resolution = float(arg.split('=')[1])
            except ValueError:
                print("Invalid resolution format. Using default 1.0")
                resolution = 1.0
    
    if resolution is None:
        resolution = 1.0
        print("No resolution provided. Using default 1.0")
    
    # Build image path
    img_name = f"Li_{resolution}.png"
    img_path = os.path.join(base_img_dir, img_name)
    
    # Load and convert image to grayscale
    if not os.path.exists(img_path):
        print(f"Error: Image not found at {img_path}")
        return
    
    img = Image.open(img_path).convert('L')
    img_array = np.array(img)
    
    # Calculate physical segment length
    x0, y0 = start_point
    x1, y1 = end_point
    pixel_length = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
    physical_length = pixel_length * resolution
    print(f"Physical segment length: {physical_length:.2f} units")
    
    # Extract grayscale values
    gray_values = get_line_grayscale(img_array, start_point, end_point)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to CSV
    csv_filename = f"grayscale_values_{resolution}.csv"
    output_path = os.path.join(output_dir, csv_filename)
    np.savetxt(output_path, gray_values, fmt='%d', delimiter=',')
    print(f"Grayscale values saved to: {output_path}")

if __name__ == '__main__':
    main()
