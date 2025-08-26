import os
import numpy as np
from PIL import Image
import argparse
import csv

# Core function: Get line grayscale values
def get_line_grayscale(image, start_point, end_point):
    """
    Uses Bresenham's line algorithm to get all pixel coordinates between start_point and end_point,
    then retrieves their grayscale values from the image.
    Returns: list of (x, y, grayscale_value)
    """
    x0, y0 = start_point
    x1, y1 = end_point

    points = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    if dx > dy:
        err = dx / 2.0
        while x != x1:
            points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
        points.append((x, y))
    else:
        err = dy / 2.0
        while y != y1:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
        points.append((x, y))

    # Get grayscale value for each point
    gray_arr = np.array(image)
    values = []
    for (x, y) in points:
        if 0 <= x < gray_arr.shape[1] and 0 <= y < gray_arr.shape[0]:
            gray_value = int(gray_arr[y, x])
            values.append([x, y, gray_value])
    return values

# Core function: Calculate u_eq (length of line in mm)
def calculate_μeq(start_point, end_point, resolution):
    """
    Returns the Euclidean distance between start and end point, times image resolution (mm/pixel)
    """
    x0, y0 = start_point
    x1, y1 = end_point
    pixel_length = np.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
    length_mm = pixel_length * resolution
    return length_mm

# Plot function: Plot grayscale values along the line
def plot_μeq_curve(values, outfile):
    import matplotlib.pyplot as plt
    grays = [v[2] for v in values]
    plt.figure()
    plt.plot(grays, marker='o')
    plt.xlabel('Point Index Along Line')
    plt.ylabel('Grayscale Value (0-255)')
    plt.title('Grayscale Along Line')
    plt.tight_layout()
    plt.savefig(outfile)
    plt.close()

def run_with_defaults():
    # Default parameters
    image_path = r'C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png'
    resolution = 0.9
    output_dir = r'C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup'
    start_point = (152, 29)
    end_point = (136, 91)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Read image and convert to grayscale
    image = Image.open(image_path).convert('L')

    # Get grayscale values along the segment
    values = get_line_grayscale(image, start_point, end_point)
    print(f"Number of points along the line: {len(values)}")
    print("First 5 grayscale values (x, y, gray):", values[:5])

    # Calculate length in mm
    eq_length = calculate_μeq(start_point, end_point, resolution)
    print(f"Line length in pixels: {np.sqrt((start_point[0]-end_point[0])**2 + (start_point[1]-end_point[1])**2):.2f}")
    print(f"Line length in mm (resolution={resolution}): {eq_length:.2f}")

    # Save grayscale values to CSV
    csv_filename = f"line_grayscale_resolution_{resolution}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    with open(csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['x', 'y', 'gray'])
        csvwriter.writerows(values)
    print(f"Saved grayscale values to {csv_path}")

    # Optionally, plot grayscale values along the line
    plot_path = os.path.join(output_dir, f"grayscale_curve_resolution_{resolution}.png")
    plot_μeq_curve(values, plot_path)
    print(f"Saved grayscale profile plot to {plot_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-image_dir', type=str, default=None, help="Path to the input image")
    parser.add_argument('-resolution', type=float, default=None, help="Image resolution in mm/pixel")
    parser.add_argument('-output_dir', type=str, default=None, help="Where to store CSV")
    args = parser.parse_args()

    # If -resolution is not given, run with defaults (as per subtask requirements)
    if args.resolution is None:
        print("No resolution specified, running with default parameters...")
        run_with_defaults()
        return

    image_path = args.image_dir if args.image_dir else r'C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png'
    resolution = args.resolution
    output_dir = args.output_dir if args.output_dir else r'C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup'
    start_point = (152, 29)
    end_point = (136, 91)

    os.makedirs(output_dir, exist_ok=True)
    image = Image.open(image_path).convert('L')
    values = get_line_grayscale(image, start_point, end_point)
    print(f"Number of points along the line: {len(values)}")
    print("First 5 grayscale values (x, y, gray):", values[:5])
    eq_length = calculate_μeq(start_point, end_point, resolution)
    print(f"Line length in pixels: {np.sqrt((start_point[0]-end_point[0])**2 + (start_point[1]-end_point[1])**2):.2f}")
    print(f"Line length in mm (resolution={resolution}): {eq_length:.2f}")
    csv_filename = f"line_grayscale_resolution_{resolution}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    with open(csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['x', 'y', 'gray'])
        csvwriter.writerows(values)
    print(f"Saved grayscale values to {csv_path}")
    plot_path = os.path.join(output_dir, f"grayscale_curve_resolution_{resolution}.png")
    plot_μeq_curve(values, plot_path)
    print(f"Saved grayscale profile plot to {plot_path}")

if __name__ == "__main__":
    main()
