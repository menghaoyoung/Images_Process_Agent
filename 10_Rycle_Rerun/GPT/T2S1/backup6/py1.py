import os
import argparse
import numpy as np
from PIL import Image
import csv
import sys
import io

# For proper UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ----------- Parameters --------------
image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup6"
start_point = (152, 29)
end_point = (136, 91)
u_max = 65535
u_min = 0


def get_line_grayscale(img, start, end):
    """
    Uses Bresenham's line algorithm to get all integer points on a line,
    and returns their grayscale values.
    """
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0

    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1

    if dx > dy:
        err = dx / 2.0
        points = []
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
        points = []
        while y != y1:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
        points.append((x, y))

    # Get grayscale values at all points
    grayscale_values = []
    for px, py in points:
        if 0 <= py < img.shape[0] and 0 <= px < img.shape[1]:
            grayscale_values.append(int(img[py, px]))
        else:
            # If out of bounds, append 0
            grayscale_values.append(0)
    return np.array(grayscale_values), points

def calculate_segment_length(start, end, resolution):
    """
    Calculate the Euclidean length of the line segment in real units using the resolution.
    """
    length_px = np.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)
    length_real = length_px * float(resolution)
    return length_px, length_real

def save_grayscale_csv(arr, out_path):
    with open(out_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(arr)
    print(f"CSV saved to: {out_path}")

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Extract grayscale values along a line in an image.')
    parser.add_argument('-resolution', type=float, required=True, help='Image resolution (unit per pixel)')
    args = parser.parse_args()

    print(f"Loading image: {image_path}")
    img = Image.open(image_path).convert('L')
    img_np = np.array(img)

    # Get grayscale values along the line
    grayscale_values, line_points = get_line_grayscale(img_np, start_point, end_point)
    print(f"Grayscale values along the line: {grayscale_values}")
    print(f"Total points along the line: {len(grayscale_values)}")

    # Calculate length
    length_px, length_real = calculate_segment_length(start_point, end_point, args.resolution)
    print(f"Line pixel length: {length_px:.2f} px")
    print(f"Line real length: {length_real:.2f} units (resolution={args.resolution})")

    # Save to CSV
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    csv_path = os.path.join(output_dir, f'grayscale_line_res{args.resolution}.csv')
    save_grayscale_csv(grayscale_values, csv_path)

    # Also print a sample of grayscale values for inspection
    print("Sample grayscale values (first 10):", grayscale_values[:10])

if __name__ == '__main__':
    main()
