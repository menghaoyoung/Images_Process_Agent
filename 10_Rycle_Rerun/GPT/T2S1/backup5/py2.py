import os
import numpy as np
import argparse
from PIL import Image
import csv
import sys
import io

# Ensure utf-8 output for print statements
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Parameters and paths
image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup3"
csv_filename = "line_grayscale_values.csv"

start_point = (152, 29)
end_point = (136, 91)
u_max = 65535
u_min = 0

def get_line_points(start, end):
    """Bresenham's line algorithm to get integer pixel coordinates along a line."""
    x1, y1 = start
    x2, y2 = end
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x2:
            points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
        points.append((x, y))
    else:
        err = dy / 2.0
        while y != y2:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
        points.append((x, y))
    return points

def get_line_grayscale(image, line_points):
    """Get grayscale values for all points along the line."""
    width, height = image.size
    gray_values = []
    for (x, y) in line_points:
        # Ensure points are within the image boundaries
        if 0 <= x < width and 0 <= y < height:
            pixel = image.getpixel((x, y))
            gray_values.append(pixel)
        else:
            gray_values.append(None)
    return gray_values

def calculate_line_length(start, end, resolution):
    """Calculate the length of the line in pixels and in physical units."""
    pixel_length = np.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
    physical_length = pixel_length * resolution
    return pixel_length, physical_length

def save_to_csv(data, csv_path):
    """Save grayscale values as an array to a CSV file."""
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['index', 'x', 'y', 'grayscale'])
        for idx, (pt, val) in enumerate(data):
            writer.writerow([idx, pt[0], pt[1], val])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-resolution', type=float, required=True, help="Image resolution (physical unit per pixel)")
    args = parser.parse_args()
    resolution = args.resolution

    # Load image
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return
    img = Image.open(image_path).convert('L')  # Convert to grayscale

    # Get points along the line
    line_points = get_line_points(start_point, end_point)
    print(f"Number of points along the line: {len(line_points)}")

    # Get grayscale values along the line
    gray_values = get_line_grayscale(img, line_points)
    print("First 10 grayscale values along the line:", gray_values[:10])

    # Calculate pixel and physical length of the line
    pixel_length, physical_length = calculate_line_length(start_point, end_point, resolution)
    print(f"Line pixel length: {pixel_length:.2f}")
    print(f"Line physical length: {physical_length:.2f}")

    # Save grayscale values to CSV
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    csv_path = os.path.join(output_dir, csv_filename)
    save_to_csv(list(zip(line_points, gray_values)), csv_path)
    print(f"Grayscale values saved to: {csv_path}")

if __name__ == "__main__":
    main()
