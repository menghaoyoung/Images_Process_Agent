import os
import numpy as np
from PIL import Image
import argparse
import csv
import sys

# --- Parameters (as constants for direct execution/testing) ---
DEFAULT_IMAGE_PATH = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
DEFAULT_OUTPUT_DIR = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup3"
DEFAULT_RESOLUTION = 0.9

START_POINT = (152, 29)
END_POINT = (136, 91)
U_MAX = 65535
U_MIN = 0

# --- Core function: Get line grayscale values ---
def get_line_grayscale(image, start_point, end_point):
    x0, y0 = start_point
    x1, y1 = end_point

    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1
    if dx > dy:
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

    grayscale_values = []
    for (x, y) in points:
        if 0 <= x < image.width and 0 <= y < image.height:
            val = image.getpixel((x, y))
            if isinstance(val, tuple):  # RGB
                val = int(np.mean(val))
            grayscale_values.append(val)
        else:
            grayscale_values.append(None)
    return grayscale_values, points

# --- Core function: Calculate μ_eq ---
def calculate_μeq(grayscale_values, u_max=U_MAX, u_min=U_MIN):
    arr = np.array(grayscale_values, dtype=np.float32)
    mask = np.array([v is not None for v in grayscale_values])
    arr[~mask] = 0  # or np.nan if you prefer
    μeq = u_min + (u_max - u_min) * (arr / 255)
    return μeq

# --- Main program execution ---
def main():
    # If no arguments, use defaults
    parser = argparse.ArgumentParser(description='Extract grayscale values along a line in an image.')
    parser.add_argument('-resolution', type=float, required=False, default=DEFAULT_RESOLUTION, help='Image resolution (pixel spacing, e.g., 0.9)')
    parser.add_argument('-image_dir', type=str, required=False, default=DEFAULT_IMAGE_PATH, help='Input image path')
    parser.add_argument('-output_dir', type=str, required=False, default=DEFAULT_OUTPUT_DIR, help='Output directory')
    args = parser.parse_args()

    image_path = args.image_dir
    output_dir = args.output_dir
    resolution = args.resolution

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load image as grayscale
    try:
        img = Image.open(image_path).convert('L')
    except Exception as e:
        print(f"Error loading image: {e}")
        sys.exit(1)
    print(f"Loaded image: {image_path}")
    print(f"Image size: {img.size}")

    # Get grayscale values along the line
    grayscale_values, points = get_line_grayscale(img, START_POINT, END_POINT)
    print(f"Extracted {len(grayscale_values)} grayscale values along the line.")

    # Calculate length of segment in physical units
    pixel_distance = np.sqrt((END_POINT[0] - START_POINT[0]) ** 2 + (END_POINT[1] - START_POINT[1]) ** 2)
    segment_length = pixel_distance * resolution
    print(f"Pixel distance: {pixel_distance:.2f}")
    print(f"Physical length: {segment_length:.2f}")

    # Calculate μ_eq values
    μeq = calculate_μeq(grayscale_values, U_MAX, U_MIN)
    print(f"First 10 grayscale values: {grayscale_values[:10]}")
    print(f"First 10 μ_eq values: {μeq[:10]}")

    # Save to CSV
    csv_filename = f'grayscale_and_μeq_res{resolution}.csv'
    csv_path = os.path.join(output_dir, csv_filename)
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x', 'y', 'Grayscale', 'μ_eq'])
        for (pt, g, m) in zip(points, grayscale_values, μeq):
            writer.writerow([pt[0], pt[1], g, m])
    print(f"Saved grayscale and μ_eq values to CSV: {csv_path}")

if __name__ == "__main__":
    main()
