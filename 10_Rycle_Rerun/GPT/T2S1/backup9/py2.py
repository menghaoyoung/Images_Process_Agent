import os
import numpy as np
import csv
import argparse
from PIL import Image

# Parameters and paths
image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup9"
start_point = (152, 29)
end_point = (136, 91)

def get_line_points(start, end):
    """
    Returns all integer (x, y) coordinates along the line from start to end (inclusive)
    using Bresenham's algorithm.
    """
    x1, y1 = start
    x2, y2 = end
    points = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1

    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1

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

def get_line_grayscale(image_arr, line_points):
    """
    Returns grayscale values (0-255) for all points along the given line.
    """
    grayscale_values = []
    for x, y in line_points:
        if 0 <= y < image_arr.shape[0] and 0 <= x < image_arr.shape[1]:
            grayscale = image_arr[y, x]
            grayscale_values.append(grayscale)
        else:
            print(f"Warning: Point ({x},{y}) is out of image bounds and will be skipped.")
    return grayscale_values

def main():
    parser = argparse.ArgumentParser(description="Extract grayscale values along a line segment in an image.")
    parser.add_argument('-resolution', type=float, required=True, help='Image resolution, e.g., 1.08')
    args = parser.parse_args()
    resolution = args.resolution

    # Output file setup
    output_filename = f'line_grayscale_values_res{resolution:.2f}.csv'
    output_path = os.path.join(output_dir, output_filename)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load image and convert to grayscale
    image = Image.open(image_path).convert('L')
    image_arr = np.array(image)
    print(f"Image loaded: {image_path}, shape: {image_arr.shape}")

    # Get line points and calculate length
    line_points = get_line_points(start_point, end_point)
    pixel_distance = np.hypot(end_point[0] - start_point[0], end_point[1] - start_point[1])
    length_mm = pixel_distance * resolution
    print(f"Line from {start_point} to {end_point}: {len(line_points)} pixels, length = {length_mm:.2f} mm (resolution = {resolution} mm/pixel)")

    # Get grayscale values along the line
    grayscale_values = get_line_grayscale(image_arr, line_points)
    print(f"First 10 grayscale values: {grayscale_values[:10]}")

    # Save to CSV
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x', 'y', 'grayscale'])
        for (x, y), val in zip(line_points, grayscale_values):
            writer.writerow([x, y, val])
    print(f"Saved grayscale values to {output_path}")

if __name__ == "__main__":
    main()
