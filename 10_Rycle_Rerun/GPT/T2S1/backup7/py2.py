import os
import sys
import csv
import argparse
import numpy as np
from PIL import Image

# Hardcoded paths and parameters as per task
image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup7"
start_point = (152, 29)
end_point = (136, 91)

def get_line_pixels(start, end):
    """
    Bresenham's line algorithm to get all integer pixel points between two points.
    Returns a list of (x, y) tuples.
    """
    x0, y0 = start
    x1, y1 = end
    points = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1

    if dx >= dy:
        err = dx / 2.0
        while x != x1:
            points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
        points.append((x1, y1))
    else:
        err = dy / 2.0
        while y != y1:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
        points.append((x1, y1))
    return points

def get_line_grayscale(img, line_points):
    """
    Returns grayscale values (0-255) for points along the line.
    """
    img_gray = img.convert('L')
    width, height = img_gray.size
    pix = img_gray.load()
    grayscale_values = []
    for x, y in line_points:
        if 0 <= x < width and 0 <= y < height:
            grayscale_values.append(pix[x, y])
        else:
            grayscale_values.append(None)  # Out of bounds
    return grayscale_values

def calculate_line_length(start, end, resolution):
    # Euclidean distance * resolution
    pixel_dist = np.hypot(end[0] - start[0], end[1] - start[1])
    length = pixel_dist * float(resolution)
    return length

def save_grayscale_to_csv(values, csv_path):
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Index", "Grayscale"])
        for idx, val in enumerate(values):
            writer.writerow([idx, val])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-resolution', type=float, required=True, help="Image resolution (e.g., mm per pixel)")
    args = parser.parse_args()
    resolution = args.resolution

    print(f"Image path: {image_path}")
    print(f"Output directory: {output_dir}")
    print(f"Start point: {start_point}")
    print(f"End point: {end_point}")
    print(f"Resolution: {resolution}")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load image
    img = Image.open(image_path)

    # Get all pixel coordinates along the line
    line_points = get_line_pixels(start_point, end_point)
    print(f"Number of points along the line: {len(line_points)}")

    # Calculate line length
    line_length = calculate_line_length(start_point, end_point, resolution)
    print(f"Line length (units): {line_length:.4f}")

    # Get grayscale values
    grayscale_values = get_line_grayscale(img, line_points)
    print("First 10 grayscale values along the line:", grayscale_values[:10])

    # Save to CSV
    csv_name = f"grayscale_line_{start_point[0]}_{start_point[1]}_{end_point[0]}_{end_point[1]}_res{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_name)
    save_grayscale_to_csv(grayscale_values, csv_path)
    print(f"Saved grayscale values to: {csv_path}")

if __name__ == '__main__':
    main()
