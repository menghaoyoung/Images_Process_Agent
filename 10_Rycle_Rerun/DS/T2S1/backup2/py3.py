import os
import numpy as np
from PIL import Image
import argparse

def bresenham_line(start, end):
    """Generate points along a line using Bresenham's algorithm."""
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    line_points = []
    
    while True:
        line_points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
            
    return line_points

def get_line_grayscale(img_array, start_point, end_point):
    """Extract grayscale values for all points along a line segment."""
    line_points = bresenham_line(start_point, end_point)
    grayscale_values = [img_array[y, x] for (x, y) in line_points]
    return grayscale_values, len(line_points)

def main():
    parser = argparse.ArgumentParser(description='Process line segment in an image.')
    parser.add_argument('--resolution', type=float, required=True, help='Resolution in units per pixel (e.g., 1.08)')
    args = parser.parse_args()
    resolution = args.resolution
    
    # Fixed parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup2"
    
    # Load image and convert to grayscale numpy array
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    
    # Get grayscale values along the line segment
    grayscale_values, num_points = get_line_grayscale(img_array, start_point, end_point)
    
    # Calculate physical length of the segment
    pixel_distance = np.sqrt((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2)
    physical_length = pixel_distance * resolution
    print(f"Physical length of segment: {physical_length:.4f} units")
    print(f"Number of points sampled: {num_points}")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save grayscale values to CSV (one value per line)
    csv_filename = f"grayscale_values_res_{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    np.savetxt(csv_path, grayscale_values, fmt='%d')
    print(f"Grayscale values saved to: {csv_path}")

if __name__ == "__main__":
    main()
