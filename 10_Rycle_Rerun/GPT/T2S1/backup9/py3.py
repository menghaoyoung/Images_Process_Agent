import os
import numpy as np
import csv
import argparse
from PIL import Image

# Hardcoded paths and parameters as per task requirements
image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup9"
start_point = (152, 29)
end_point = (136, 91)

def get_line_points(start, end):
    """Get list of (x, y) coordinates between start and end pixel, inclusive."""
    x1, y1 = start
    x2, y2 = end
    points = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1
    err = dx - dy

    x, y = x1, y1
    while True:
        points.append((x, y))
        if x == x2 and y == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return points

def get_line_grayscale(image_arr, line_points):
    """Return grayscale values (0-255) for all points along the given line."""
    grayscale_values = []
    for x, y in line_points:
        if 0 <= y < image_arr.shape[0] and 0 <= x < image_arr.shape[1]:
            grayscale = int(image_arr[y, x])
            grayscale_values.append(grayscale)
        else:
            print(f"Warning: Point ({x},{y}) is out of image bounds and will be skipped.")
    return grayscale_values

def main():
    parser = argparse.ArgumentParser(description="Extract grayscale values along a line segment in an image.")
    parser.add_argument('-resolution', type=float, required=True, help='Image resolution, e.g., 1.08')
    args = parser.parse_args()

    resolution = args.resolution

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    output_filename = f'line_grayscale_values_res{resolution:.2f}.csv'
    output_path = os.path.join(output_dir, output_filename)

    # Load image and convert to grayscale
    image = Image.open(image_path).convert('L')
    image_arr = np.array(image)
    print("Image loaded:", image_path)
    print("Image shape:", image_arr.shape)

    # Get all integer points along the line
    line_points = get_line_points(start_point, end_point)
    print(f"Number of points along the line: {len(line_points)}")

    # Calculate physical length of the line
    pixel_distance = np.hypot(end_point[0] - start_point[0], end_point[1] - start_point[1])
    length_mm = pixel_distance * resolution
    print(f"Line pixel distance: {pixel_distance:.2f} px, Physical length: {length_mm:.2f} mm (resolution {resolution} mm/pixel)")

    # Get grayscale values
    grayscale_values = get_line_grayscale(image_arr, line_points)
    print("First 10 grayscale values:", grayscale_values[:10])

    # Save as CSV
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x', 'y', 'grayscale'])
        for (x, y), gray in zip(line_points, grayscale_values):
            writer.writerow([x, y, gray])
    print(f"Saved grayscale values to {output_path}")

if __name__ == "__main__":
    main()
