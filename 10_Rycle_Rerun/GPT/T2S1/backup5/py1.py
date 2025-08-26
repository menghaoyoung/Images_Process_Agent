import os
import numpy as np
import argparse
from PIL import Image
import csv

# Parameters
image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup3"
csv_filename = "line_grayscale_values.csv"  # Output CSV file name

start_point = (152, 29)
end_point = (136, 91)
u_max = 65535
u_min = 0

def get_line_points(start, end):
    """Bresenham's Line Algorithm to get (x, y) coordinates between start and end (inclusive)"""
    x1, y1 = start
    x2, y2 = end

    points = []
    dx = abs(x2 - x1)
    dy = -abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx + dy  # error value e_xy

    while True:
        points.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x1 += sx
        if e2 <= dx:
            err += dx
            y1 += sy
    return points

def get_line_grayscale(image, line_points):
    """Get grayscale values for all points along the line"""
    width, height = image.size
    gray_values = []
    for (x, y) in line_points:
        # Ensure points are within image boundaries
        if 0 <= x < width and 0 <= y < height:
            pixel = image.getpixel((x, y))  # This will be int for L mode
            gray_values.append(pixel)
        else:
            gray_values.append(None)  # Out of bounds, mark as None
    return gray_values

def calculate_line_length(start, end, resolution):
    """Calculate the physical length of the line (in units, e.g., mm)"""
    pixel_length = np.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)
    physical_length = pixel_length * resolution
    return pixel_length, physical_length

def save_to_csv(data, csv_path):
    """Save grayscale values array to CSV"""
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

    # 1. Load image
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return
    img = Image.open(image_path)
    img = img.convert('L')  # Ensure grayscale

    # 2. Get points along the line
    line_points = get_line_points(start_point, end_point)
    print(f"Number of points along the line: {len(line_points)}")

    # 3. Get grayscale values along the line
    gray_values = get_line_grayscale(img, line_points)
    print("First 10 grayscale values along the line:", gray_values[:10])

    # 4. Calculate line length in pixels and physical units
    pixel_length, physical_length = calculate_line_length(start_point, end_point, resolution)
    print(f"Line pixel length: {pixel_length:.2f}")
    print(f"Line physical length (unit): {physical_length:.2f}")

    # 5. Save grayscale values to CSV
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    csv_path = os.path.join(output_dir, csv_filename)
    save_to_csv(list(zip(line_points, gray_values)), csv_path)
    print(f"Grayscale values saved to: {csv_path}")

if __name__ == "__main__":
    main()
