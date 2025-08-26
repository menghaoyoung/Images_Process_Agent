import os
import numpy as np
from PIL import Image
import sys
import math

def bresenham_line(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1
    dx = abs(dx)
    dy = abs(dy)
    
    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0
    
    D = 2 * dy - dx
    y = 0
    points = []
    for x in range(dx + 1):
        points.append((x0 + x * xx + y * yx, y0 + x * xy + y * yy))
        if D >= 0:
            y += 1
            D -= 2 * dx
        D += 2 * dy
    return points

def main():
    resolution_value = None
    for arg in sys.argv[1:]:
        if arg.startswith('-resolution='):
            resolution_str = arg.split('=')[1]
            try:
                resolution_value = float(resolution_str)
            except ValueError:
                sys.exit("Error: Resolution must be a number.")
            break
    if resolution_value is None:
        sys.exit("Usage: python py1.py -resolution=<value>")
    
    input_base_dir = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS"
    output_base_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup1"
    image_path = os.path.join(input_base_dir, f"Li_{resolution_str}.png")
    os.makedirs(output_base_dir, exist_ok=True)
    output_file = os.path.join(output_base_dir, f"grayscale_values_{resolution_str}.csv")
    
    try:
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
    except FileNotFoundError:
        sys.exit(f"Error: Image not found at {image_path}")
    except Exception as e:
        sys.exit(f"Error loading image: {str(e)}")
    
    start_point = (152, 29)
    end_point = (136, 91)
    
    line_points = bresenham_line(start_point[0], start_point[1], end_point[0], end_point[1])
    
    grayscale_values = []
    for x, y in line_points:
        if 0 <= y < img_array.shape[0] and 0 <= x < img_array.shape[1]:
            grayscale_values.append(str(img_array[y, x]))
        else:
            grayscale_values.append('0')
    
    pixel_distance = math.sqrt((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2)
    physical_length = pixel_distance * resolution_value
    print(f"Physical length: {physical_length:.2f} units")
    
    with open(output_file, 'w') as f:
        f.write("\n".join(grayscale_values))
    print(f"Grayscale values saved to: {output_file}")

if __name__ == '__main__':
    main()
