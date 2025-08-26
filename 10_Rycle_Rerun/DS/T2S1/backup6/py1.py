import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import io
import math

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Helper function: Bresenham's line algorithm
def bresenham_line(x0, y0, x1, y1):
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

# Core function: Get line grayscale values
def get_line_grayscale(img_array, start_point, end_point):
    x0, y0 = start_point
    x1, y1 = end_point
    line_points = bresenham_line(x0, y0, x1, y1)
    values = []
    for (x, y) in line_points:
        if 0 <= y < img_array.shape[0] and 0 <= x < img_array.shape[1]:
            values.append(img_array[y, x])
        else:
            values.append(0)
    return values

# Main program execution
def main():
    resolution = None
    for arg in sys.argv[1:]:
        if arg.startswith('-resolution='):
            resolution = float(arg.split('=')[1])
            break
    
    if resolution is None:
        print("Error: Resolution not provided. Use -resolution=<value>")
        sys.exit(1)
    
    # Construct image path using resolution
    base_img_dir = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS"
    image_path = os.path.join(base_img_dir, f"Li_{resolution}.png")
    start_point = (152, 29)
    end_point = (136, 91)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup6"
    
    try:
        # Open and process image
        img = Image.open(image_path)
        if img.mode != 'L':
            img = img.convert('L')
        img_array = np.array(img)
        
        # Get grayscale values
        grayscale_values = get_line_grayscale(img_array, start_point, end_point)
        
        # Calculate physical length
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        pixel_distance = math.sqrt(dx**2 + dy**2)
        physical_length = pixel_distance * resolution
        print(f"Physical length: {physical_length:.2f} units")
        
        # Save results to CSV
        os.makedirs(output_dir, exist_ok=True)
        csv_filename = os.path.join(output_dir, f"grayscale_values_res_{resolution}.csv")
        with open(csv_filename, 'w') as f:
            for val in grayscale_values:
                f.write(f"{val}\n")
        print(f"Grayscale values saved to: {csv_filename}")
        
    except FileNotFoundError:
        print(f"Error: Image not found at {image_path}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
