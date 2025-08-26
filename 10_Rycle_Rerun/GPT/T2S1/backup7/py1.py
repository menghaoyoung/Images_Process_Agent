import os
import sys
import csv
import argparse
import numpy as np
from PIL import Image

# Set up paths and parameters
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
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy  # error value e_xy

    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
    return points

def get_line_grayscale(img, line_points):
    """
    Returns grayscale values (0-255) for points along the line.
    """
    img_gray = img.convert('L')
    pix = img_gray.load()
    grayscale_values = []
    for x, y in line_points:
        if 0 <= x < img_gray.width and 0 <= y < img_gray.height:
            grayscale_values.append(pix[x, y])
        else:
            grayscale_values.append(None)  # Out of bounds
    return grayscale_values

def calculate_line_length(start, end, resolution):
    # Euclidean distance * resolution (e.g., mm/pixel)
    pixel_dist = np.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)
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
    print(f"Output dir: {output_dir}")
    print(f"Start point: {start_point}")
    print(f"End point: {end_point}")
    print(f"Resolution: {resolution}")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    img = Image.open(image_path)
    # Get all pixel coordinates along the line
    line_points = get_line_pixels(start_point, end_point)
    print(f"Total number of points along the line: {len(line_points)}")

    # Calculate line length
    line_length = calculate_line_length(start_point, end_point, resolution)
    print(f"Line length (in units of resolution): {line_length:.3f}")

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
