import os
import numpy as np
import csv
from PIL import Image
import argparse

# Core function: Get line grayscale values
def get_line_grayscale(img, start_point, end_point):
    """
    Given a PIL Image (assumed grayscale), and start/end points,
    sample all points along the line and return their grayscale values (0-255).
    Uses Bresenham's line algorithm.
    """
    x1, y1 = start_point
    x2, y2 = end_point
    # Get all pixel coordinates along the line using Bresenham's algorithm
    points = []
    dx = abs(x2 - x1)
    dy = -abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx + dy  # error value e_xy
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

    # Get grayscale values at these points
    gray_array = []
    for x, y in points:
        # Clamp to image size
        if x < 0 or x >= img.width or y < 0 or y >= img.height:
            gray = 0
        else:
            gray = img.getpixel((x, y))
        gray_array.append(gray)
    length_in_pixels = len(points)
    return gray_array, length_in_pixels

def save_to_csv(gray_array, csv_path):
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Index', 'Grayscale'])
        for idx, val in enumerate(gray_array):
            writer.writerow([idx, val])

# Main program execution
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-resolution', type=float, required=True, help='Resolution in um/pixel')
    parser.add_argument('-image_dir', type=str, default=r'C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png')
    parser.add_argument('-output_dir', type=str, default=r'C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup8')
    parser.add_argument('-start', type=str, default='152,29')
    parser.add_argument('-end', type=str, default='136,91')
    args = parser.parse_args()

    image_path = args.image_dir
    output_dir = args.output_dir
    start_point = tuple(map(int, args.start.split(',')))
    end_point = tuple(map(int, args.end.split(',')))

    # Load image
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return
    img = Image.open(image_path).convert('L')  # grayscale

    print(f"Loaded image: {image_path}")

    # Calculate grayscale values along the line
    gray_array, length_pixels = get_line_grayscale(img, start_point, end_point)

    # Calculate length in micrometers
    real_length = length_pixels * args.resolution
    print(f"Line segment from {start_point} to {end_point}:")
    print(f" - Pixels traversed: {length_pixels}")
    print(f" - Length (um): {real_length:.3f}")

    print("Grayscale values along line segment:")
    print(gray_array)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    # Output file name: based on image name, resolution, and line points
    img_name = os.path.splitext(os.path.basename(image_path))[0]
    out_csv = os.path.join(output_dir, f"{img_name}_line_{start_point[0]}_{start_point[1]}_{end_point[0]}_{end_point[1]}_res{args.resolution:.2f}.csv")

    save_to_csv(gray_array, out_csv)
    print(f"Grayscale array saved to CSV: {out_csv}")

if __name__ == '__main__':
    main()
