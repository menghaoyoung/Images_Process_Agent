import os
import numpy as np
import argparse
from PIL import Image
import csv
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Input image path and parameters
image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
start_point = (152, 29)
end_point = (136, 91)
u_max = 65535
u_min = 0

# Output directory and filename
output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup3"
output_csv = os.path.join(output_dir, "line_grayscale_values.csv")

def get_line_points(start, end):
    """
    Get all integer (x, y) pixel coordinates along a line segment using linear interpolation.
    """
    x0, y0 = start
    x1, y1 = end
    length = int(np.hypot(x1 - x0, y1 - y0)) + 1
    x_values = np.linspace(x0, x1, length)
    y_values = np.linspace(y0, y1, length)
    points = list(zip(np.round(x_values).astype(int), np.round(y_values).astype(int)))
    return points

def get_line_grayscale(image, points):
    """
    Given PIL image and list of (x, y) points, return grayscale values (0-255) along the line.
    """
    if image.mode != 'L':
        image = image.convert('L')
    img_arr = np.array(image)
    grayscale_values = []
    for (x, y) in points:
        if 0 <= x < img_arr.shape[1] and 0 <= y < img_arr.shape[0]:
            grayscale_values.append(int(img_arr[y, x]))
        else:
            grayscale_values.append(None)
    return np.array(grayscale_values)

def calculate_line_length(start, end, resolution):
    """
    Calculate the real-world length of the line segment using resolution (mm/pixel).
    """
    pixel_length = np.hypot(end[0] - start[0], end[1] - start[1])
    real_length = pixel_length * resolution
    return pixel_length, real_length

def save_grayscale_to_csv(grayscale_values, csv_path):
    """
    Save grayscale values as a single row in a CSV file.
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(grayscale_values.tolist())
    print(f"Grayscale values saved to {csv_path}")

def main(resolution):
    # Load image
    print(f"Loading image from {image_path}")
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)

    # Get points along the line
    points = get_line_points(start_point, end_point)
    print(f"Number of points along line: {len(points)}")

    # Get grayscale values along the line
    grayscale_values = get_line_grayscale(image, points)

    # Print the grayscale values
    print("Grayscale values along line segment:")
    print(grayscale_values)

    # Save grayscale values to CSV
    save_grayscale_to_csv(grayscale_values, output_csv)

    # Calculate and print line lengths
    pixel_length, real_length = calculate_line_length(start_point, end_point, resolution)
    print(f"Line segment pixel length: {pixel_length:.2f}")
    print(f"Line segment real-world length (resolution={resolution}): {real_length:.2f}")

if __name__ == "__main__":
    # This allows passing resolution either via command-line or interactively if not provided
    parser = argparse.ArgumentParser(description="Extract line grayscale values from image.")
    parser.add_argument('-resolution', type=float, help="Image resolution (e.g., mm/pixel)")
    args, unknown = parser.parse_known_args()

    if args.resolution is not None:
        main(args.resolution)
    else:
        # If not provided as argument, prompt interactively
        try:
            resolution = float(input("Please enter the image resolution (e.g., mm/pixel): "))
            main(resolution)
        except Exception as e:
            print("Error: You must provide a valid resolution value (float).")
            sys.exit(1)
