import os
import numpy as np
import argparse
from PIL import Image
import math

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-resolution', type=float, required=True, help='Resolution value (e.g., 1.08)')
    args = parser.parse_args()
    
    resolution = args.resolution
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup7"
    
    os.makedirs(output_dir, exist_ok=True)
    image = Image.open(image_path).convert('L')
    
    dx = start_point[0] - end_point[0]
    dy = start_point[1] - end_point[1]
    distance_pixels = math.sqrt(dx**2 + dy**2)
    physical_length = distance_pixels * resolution
    print(f"Physical length of the segment: {physical_length:.2f} units")
    
    points = bresenham(start_point[0], start_point[1], end_point[0], end_point[1])
    grayscale_values = [image.getpixel((x, y)) for (x, y) in points]
    
    csv_filename = f"grayscale_values_res_{resolution}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    np.savetxt(csv_path, grayscale_values, fmt='%d', delimiter=',')
    print(f"Grayscale values for {len(grayscale_values)} points saved to {csv_path}")

if __name__ == '__main__':
    main()
