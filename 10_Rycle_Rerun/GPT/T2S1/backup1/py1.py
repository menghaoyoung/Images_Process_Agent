import os
import numpy as np
from PIL import Image
import argparse
import csv

# Core function: Get line grayscale values
def get_line_grayscale(image, start_point, end_point):
    """
    Returns grayscale values (0-255) along the line from start_point to end_point.
    Uses Bresenham's algorithm for line traversal.
    """
    x0, y0 = start_point
    x1, y1 = end_point

    # PIL images use (x, y) = (col, row)
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0

    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1

    grayscale_values = []

    if dx > dy:
        err = dx / 2.0
        while x != x1:
            pixel = image.getpixel((x, y))
            if isinstance(pixel, tuple):  # RGB or RGBA image
                # Convert to grayscale with standard weights
                pixel = int(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])
            grayscale_values.append(pixel)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            pixel = image.getpixel((x, y))
            if isinstance(pixel, tuple):
                pixel = int(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])
            grayscale_values.append(pixel)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy

    # Add the end point
    pixel = image.getpixel((x1, y1))
    if isinstance(pixel, tuple):
        pixel = int(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])
    grayscale_values.append(pixel)
    return grayscale_values

# Core function: Calculate μ_eq (length of the segment in mm)
def calculate_μeq(start_point, end_point, resolution):
    """
    Calculates the physical length of the line segment based on image resolution.
    """
    x0, y0 = start_point
    x1, y1 = end_point
    pixel_length = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
    real_length = pixel_length * resolution
    return real_length

# Main program execution
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-image_dir", type=str, default=r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png", help="Path to the input image")
    parser.add_argument("-resolution", type=float, required=True, help="Image resolution (mm per pixel)")
    parser.add_argument("-output_dir", type=str, default=r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup1", help="Directory to save output CSV")
    parser.add_argument("-start_point", type=str, default="152,29", help="Start point (x,y)")
    parser.add_argument("-end_point", type=str, default="136,91", help="End point (x,y)")
    args = parser.parse_args()

    image_path = args.image_dir
    resolution = args.resolution
    output_dir = args.output_dir
    start_point = tuple(map(int, args.start_point.split(",")))
    end_point = tuple(map(int, args.end_point.split(",")))

    # Load image
    img = Image.open(image_path)
    if img.mode != 'L':
        img = img.convert('L')  # Convert to grayscale

    print(f"Image loaded from: {image_path}")
    print(f"Start point: {start_point}, End point: {end_point}")

    # Get grayscale values along the line
    grayscale_values = get_line_grayscale(img, start_point, end_point)
    print(f"Number of points along line: {len(grayscale_values)}")
    print("Sample grayscale values (first 10):", grayscale_values[:10])

    # Calculate length of the line in mm
    line_length_mm = calculate_μeq(start_point, end_point, resolution)
    print(f"Line length (in mm): {line_length_mm:.3f}")

    # Prepare output
    os.makedirs(output_dir, exist_ok=True)
    output_csv = os.path.join(output_dir, "line_grayscale_values.csv")
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Index", "Grayscale_value"])
        for idx, value in enumerate(grayscale_values):
            writer.writerow([idx, value])
    print(f"Grayscale values saved to: {output_csv}")

    # Also save the length info
    output_len = os.path.join(output_dir, "line_length_mm.txt")
    with open(output_len, 'w') as f:
        f.write(f"Line length (mm): {line_length_mm:.6f}\n")
    print(f"Line length saved to: {output_len}")

if __name__ == "__main__":
    main()
