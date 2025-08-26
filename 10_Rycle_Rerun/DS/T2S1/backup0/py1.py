import os
import numpy as np
import argparse
from PIL import Image

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

def get_line_grayscale(image_array, start, end):
    """Get grayscale values for all points along a line segment"""
    x0, y0 = start
    x1, y1 = end
    line_points = bresenham_line(x0, y0, x1, y1)
    values = []
    for (x, y) in line_points:
        if 0 <= y < image_array.shape[0] and 0 <= x < image_array.shape[1]:
            values.append(image_array[y, x])
        else:
            values.append(0)
    return values

def main():
    # Parse command-line argument for resolution
    parser = argparse.ArgumentParser()
    parser.add_argument("-resolution", type=float, required=True)
    args = parser.parse_args()
    resolution = args.resolution

    # Fixed parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup"

    # Load and process image
    image = Image.open(image_path)
    if image.mode != 'L':
        image = image.convert('L')
    img_array = np.array(image)

    # Calculate physical line length
    x0, y0 = start_point
    x1, y1 = end_point
    pixel_length = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
    physical_length = pixel_length * resolution
    print(f"Physical line length: {physical_length:.2f} units")

    # Extract grayscale values
    grayscale_values = get_line_grayscale(img_array, start_point, end_point)

    # Save to CSV
    os.makedirs(output_dir, exist_ok=True)
    csv_filename = os.path.join(output_dir, f"grayscale_values_res_{resolution:.2f}.csv")
    
    with open(csv_filename, 'w') as f:
        for value in grayscale_values:
            f.write(f"{value}\n")
    
    print(f"CSV file created: {csv_filename}")

if __name__ == "__main__":
    main()
