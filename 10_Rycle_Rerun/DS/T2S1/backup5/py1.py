import os
import numpy as np
from PIL import Image
import sys
import math
import argparse

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-resolution', type=float, required=True)
    args = parser.parse_args()
    resolution = args.resolution
    
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup5"
    os.makedirs(output_dir, exist_ok=True)
    
    start_point = (152, 29)
    end_point = (136, 91)
    
    img = Image.open(image_path)
    if img.mode != 'L':
        img = img.convert('L')
    img_array = np.array(img)
    
    x0, y0 = start_point
    x1, y1 = end_point
    line_coords = bresenham_line(x0, y0, x1, y1)
    
    grayscale_values = []
    for x, y in line_coords:
        if 0 <= y < img_array.shape[0] and 0 <= x < img_array.shape[1]:
            grayscale_values.append(img_array[y, x])
        else:
            grayscale_values.append(0)
    
    pixel_distance = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
    real_length = pixel_distance * resolution
    print(f"Real length: {real_length}")
    
    filename = f"grayscale_values_res_{str(resolution).replace('.', '_')}.csv"
    output_path = os.path.join(output_dir, filename)
    np.savetxt(output_path, grayscale_values, fmt='%d', delimiter=',')
    print(f"CSV file saved to: {output_path}")

if __name__ == "__main__":
    main()
