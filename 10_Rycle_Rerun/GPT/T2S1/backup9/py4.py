import os
import numpy as np
import csv
import sys
from PIL import Image

# ------------------- USER PARAMETERS -------------------
image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup9"
start_point = (152, 29)
end_point = (136, 91)
# -------------------------------------------------------

def get_line_points(start, end):
    """Returns a list of (x, y) tuples along a line from start to end using Bresenham's algorithm."""
    x1, y1 = start
    x2, y2 = end
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
    return points

def get_line_grayscale(image_arr, line_points):
    """Return grayscale values (0-255) for all points along the given line."""
    grayscale_values = []
    for x, y in line_points:
        if 0 <= x < image_arr.shape[1] and 0 <= y < image_arr.shape[0]:
            grayscale = int(image_arr[y, x])
            grayscale_values.append(grayscale)
        else:
            print(f"Warning: Point ({x},{y}) is out of bounds and will be skipped.")
    return grayscale_values

def main():
    # --------- COMMAND LINE ARGUMENTS -----------
    if len(sys.argv) != 3 or not sys.argv[1].startswith("-resolution"):
        print("Usage: python py3.py -resolution <float>")
        sys.exit(1)
    try:
        resolution = float(sys.argv[2])
    except ValueError:
        print("Error: resolution must be a floating point number.")
        sys.exit(1)
    # --------------------------------------------

    # Prepare output path
    os.makedirs(output_dir, exist_ok=True)
    output_fname = f'line_grayscale_values_res{resolution:.2f}.csv'
    output_path = os.path.join(output_dir, output_fname)

    # Load and convert image
    image = Image.open(image_path).convert('L')
    image_arr = np.array(image)
    print(f"Image loaded: {image_path}")
    print(f"Image shape: {image_arr.shape}")

    # Get line points and grayscale values
    points = get_line_points(start_point, end_point)
    grays = get_line_grayscale(image_arr, points)
    print(f"Extracted {len(grays)} grayscale values along line.")
    print(f"First 10 grayscale values: {grays[:10]}")

    # Calculate length
    pixel_dist = np.hypot(end_point[0] - start_point[0], end_point[1] - start_point[1])
    length_mm = pixel_dist * resolution
    print(f"Line pixel distance: {pixel_dist:.2f} px, Physical length: {length_mm:.2f} mm")

    # Save CSV
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['x', 'y', 'grayscale'])
        for (x, y), g in zip(points, grays):
            writer.writerow([x, y, g])
    print(f"Grayscale values saved to {output_path}")

if __name__ == "__main__":
    main()
