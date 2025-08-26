import os
import numpy as np
import argparse
from PIL import Image
import csv

# Parameters (hardcoded as per task, modify here if needed)
image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
start_point = (152, 29)
end_point = (136, 91)
u_max = 65535
u_min = 0

# Output directory
output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup3"
output_csv = os.path.join(output_dir, "line_grayscale_values.csv")

def get_line_points(start, end):
    """
    Use Bresenham's algorithm or np.linspace to get all pixel coordinates along the line segment.
    Returns a list of (x, y) tuples (integers).
    """
    x0, y0 = start
    x1, y1 = end
    # Number of points as the maximum of delta x or y + 1
    length = int(np.hypot(x1 - x0, y1 - y0)) + 1
    x_values = np.linspace(x0, x1, length)
    y_values = np.linspace(y0, y1, length)
    points = list(zip(np.round(x_values).astype(int), np.round(y_values).astype(int)))
    return points

def get_line_grayscale(image, points):
    """
    Given PIL image and list of (x, y) points, return grayscale values (0-255) along the line.
    """
    # Convert to grayscale if not already
    if image.mode != 'L':
        image = image.convert('L')
    img_arr = np.array(image)
    grayscale_values = []
    for (x, y) in points:
        # Check bounds
        if 0 <= x < img_arr.shape[1] and 0 <= y < img_arr.shape[0]:
            grayscale = img_arr[y, x]
            grayscale_values.append(grayscale)
        else:
            grayscale_values.append(None)  # or np.nan, if you want to handle it later
    return np.array(grayscale_values)

def calculate_line_length(start, end, resolution):
    """
    Calculate the real-world length of the line segment using resolution (e.g., mm/pixel).
    """
    pixel_length = np.hypot(end[0] - start[0], end[1] - start[1])
    real_length = pixel_length * resolution
    return pixel_length, real_length

def save_grayscale_to_csv(grayscale_values, csv_path):
    """
    Save grayscale values as an array (single row) in a CSV file.
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(grayscale_values)
    print(f"Grayscale values saved to {csv_path}")

def main():
    parser = argparse.ArgumentParser(description="Extract line grayscale values from image.")
    parser.add_argument('-resolution', type=float, required=True, help="Image resolution (e.g., mm/pixel)")
    args = parser.parse_args()

    # Load image
    print(f"Loading image from {image_path}")
    image = Image.open(image_path)

    # Get all points along the line segment
    points = get_line_points(start_point, end_point)
    print(f"Number of points along line: {len(points)}")

    # Get grayscale values (0-255) along the line
    grayscale_values = get_line_grayscale(image, points)

    # Print the grayscale values
    print("Grayscale values along line segment:")
    print(grayscale_values)

    # Save to CSV
    save_grayscale_to_csv(grayscale_values, output_csv)

    # Calculate and print line length
    pixel_length, real_length = calculate_line_length(start_point, end_point, args.resolution)
    print(f"Line segment pixel length: {pixel_length:.2f}")
    print(f"Line segment real-world length (resolution={args.resolution}): {real_length:.2f}")

if __name__ == "__main__":
    main()
