import os
import numpy as np
from PIL import Image
import sys
import math

def bresenham_line(x0, y0, x1, y1):
    """Generate points along a line using Bresenham's algorithm"""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    points = []
    
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
    # Directly handle command-line arguments
    resolution_value = None
    resolution_str = None
    
    # Process each argument looking for -resolution pattern
    for arg in sys.argv[1:]:
        if arg.startswith('-resolution='):
            resolution_str = arg.split('=', 1)[1]
            try:
                resolution_value = float(resolution_str)
            except ValueError:
                sys.exit(f"Error: Invalid resolution value '{resolution_str}'. Must be a number.")
            break
    
    if resolution_value is None:
        sys.exit("Usage: python py1.py -resolution=<value> (e.g. -resolution=1.08)")
    
    # Configure paths
    input_base_dir = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS"
    output_base_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup1"
    os.makedirs(output_base_dir, exist_ok=True)
    
    # Build image path and output file path
    image_path = os.path.join(input_base_dir, f"Li_{resolution_str}.png")
    output_file = os.path.join(output_base_dir, f"grayscale_values_{resolution_str}.csv")
    
    # Load and process image
    try:
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
    except FileNotFoundError:
        sys.exit(f"Error: Image not found at {image_path}")
    except Exception as e:
        sys.exit(f"Error loading image: {str(e)}")
    
    # Define line segment points (fixed positions)
    start_point = (152, 29)
    end_point = (136, 91)
    
    # Get all points along the line
    line_points = bresenham_line(*start_point, *end_point)
    
    # Collect grayscale values along the line
    grayscale_values = []
    for point in line_points:
        x, y = point
        if 0 <= y < img_array.shape[0] and 0 <= x < img_array.shape[1]:
            grayscale_values.append(str(img_array[y, x]))
        else:
            grayscale_values.append('0')  # Handle out-of-bound points
    
    # Calculate physical length
    dx = end_point[0] - start_point[0]
    dy = end_point[1] - start_point[1]
    pixel_distance = math.sqrt(dx**2 + dy**2)
    physical_length = pixel_distance * resolution_value
    print(f"Physical length: {physical_length:.2f} units")
    
    # Save to CSV
    with open(output_file, 'w') as f:
        f.write("\n".join(grayscale_values))
    print(f"Success: Saved {len(grayscale_values)} grayscale values to {output_file}")

if __name__ == '__main__':
    main()
