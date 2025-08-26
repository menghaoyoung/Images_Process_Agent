import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import io
import argparse
import math

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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

def get_line_grayscale(img_array, start_point, end_point):
    x0, y0 = start_point
    x1, y1 = end_point
    line_points = bresenham_line(x0, y0, x1, y1)
    values = []
    for (x, y) in line_points:
        values.append(img_array[y, x])
    return values

def main():
    parser = argparse.ArgumentParser(description='Process line grayscale values.')
    parser.add_argument('-resolution', type=float, required=True, help='Resolution value (e.g., 1.08)')
    args = parser.parse_args()
    resolution = args.resolution
    
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup9"
    
    os.makedirs(output_dir, exist_ok=True)
    
    img = Image.open(image_path)
    if img.mode != 'L':
        img = img.convert('L')
    img_array = np.array(img)
    
    dx = end_point[0] - start_point[0]
    dy = end_point[1] - start_point[1]
    pixel_length = math.sqrt(dx**2 + dy**2)
    physical_length = pixel_length * resolution
    print(f"Physical length of the segment: {physical_length:.2f} units")
    
    grayscale_values = get_line_grayscale(img_array, start_point, end_point)
    
    output_csv = os.path.join(output_dir, f"grayscale_values_res_{resolution:.2f}.csv")
    np.savetxt(output_csv, grayscale_values, delimiter=',', fmt='%d')
    print(f"Saved grayscale values to {output_csv}")
    print("Calculation successful")

if __name__ == "__main__":
    main()
