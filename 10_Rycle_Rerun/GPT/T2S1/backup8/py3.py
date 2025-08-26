import os
import numpy as np
import csv
from PIL import Image
import argparse

def get_line_grayscale(img, start_point, end_point):
    """
    Get grayscale values (0-255) for all pixel points along a line segment.
    Uses Bresenham's algorithm.
    """
    x1, y1 = start_point
    x2, y2 = end_point
    points = []
    dx = abs(x2 - x1)
    dy = -abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx + dy
    x, y = x1, y1
    while True:
        points.append((x, y))
        if x == x2 and y == y2:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy

    gray_array = []
    for x, y in points:
        if 0 <= x < img.width and 0 <= y < img.height:
            gray = img.getpixel((x, y))
        else:
            gray = 0
        gray_array.append(gray)
    return gray_array, len(points)

def save_to_csv(gray_array, csv_path):
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Index', 'Grayscale'])
        for idx, val in enumerate(gray_array):
            writer.writerow([idx, val])

def main():
    # Set default parameters according to the task description
    default_image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    default_output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup8"
    default_start = "152,29"
    default_end = "136,91"
    default_resolution = 0.9

    parser = argparse.ArgumentParser()
    parser.add_argument('-resolution', type=float, default=default_resolution, help='Resolution in um/pixel')
    parser.add_argument('-image_dir', type=str, default=default_image_path, help='Input image path')
    parser.add_argument('-output_dir', type=str, default=default_output_dir, help='Directory for CSV output')
    parser.add_argument('-start', type=str, default=default_start, help='Start point as x,y')
    parser.add_argument('-end', type=str, default=default_end, help='End point as x,y')
    args = parser.parse_args()

    image_path = args.image_dir
    output_dir = args.output_dir
    try:
        start_point = tuple(map(int, args.start.strip().split(',')))
        end_point = tuple(map(int, args.end.strip().split(',')))
    except Exception as e:
        print("Error parsing start/end points. Please use 'x,y' format.")
        return

    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return
    img = Image.open(image_path).convert('L')
    print(f"Loaded image: {image_path}")

    gray_array, length_pixels = get_line_grayscale(img, start_point, end_point)
    real_length = length_pixels * args.resolution
    print(f"Line segment from {start_point} to {end_point}:")
    print(f" - Pixels traversed: {length_pixels}")
    print(f" - Length (um): {real_length:.3f}")
    print("Grayscale values along line segment:")
    print(gray_array)

    os.makedirs(output_dir, exist_ok=True)
    img_name = os.path.splitext(os.path.basename(image_path))[0]
    out_csv = os.path.join(
        output_dir,
        f"{img_name}_line_{start_point[0]}_{start_point[1]}_{end_point[0]}_{end_point[1]}_res{args.resolution:.2f}.csv"
    )
    save_to_csv(gray_array, out_csv)
    print(f"Grayscale array saved to CSV: {out_csv}")

if __name__ == '__main__':
    main()
