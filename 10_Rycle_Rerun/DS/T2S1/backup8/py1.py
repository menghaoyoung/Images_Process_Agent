import os
import sys
import math
from PIL import Image

def bresenham(start, end):
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    points = []
    
    if dx > dy:
        err = dx / 2.0
        y = y0
        x = x0
        step = 1 if x1 > x0 else -1
        x_target = x1 + step
        while x != x_target:
            points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        x = x0
        y = y0
        step = 1 if y1 > y0 else -1
        y_target = y1 + step
        while y != y_target:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    return points

def get_line_grayscale(image, start, end):
    points = bresenham(start, end)
    grayscale_vals = []
    for (x, y) in points:
        if 0 <= x < image.width and 0 <= y < image.height:
            grayscale_vals.append(image.getpixel((x, y)))
        else:
            grayscale_vals.append(0)
    return grayscale_vals

def main():
    resolution = None
    for arg in sys.argv[1:]:
        if arg.startswith('-resolution='):
            try:
                resolution = float(arg.split('=')[1])
            except ValueError:
                print("Error: Resolution value must be a number.")
                sys.exit(1)
    
    if resolution is None:
        print("Error: Resolution not provided. Use -resolution=<value>")
        sys.exit(1)
        
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup8"
    start_point = (152, 29)
    end_point = (136, 91)
    
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        sys.exit(1)
    
    try:
        image = Image.open(image_path)
        if image.mode != 'L':
            image = image.convert('L')
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)
    
    grayscale_vals = get_line_grayscale(image, start_point, end_point)
    
    pixel_dist = math.sqrt((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2)
    real_length = pixel_dist * resolution
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    csv_filename = f"line_gray_values_res_{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    try:
        with open(csv_path, 'w') as f:
            for val in grayscale_vals:
                f.write(f"{val}\n")
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        sys.exit(1)
    
    print(f"Real length of the segment: {real_length:.2f} units")
    print(f"Saved grayscale values to: {csv_path}")

if __name__ == "__main__":
    main()
