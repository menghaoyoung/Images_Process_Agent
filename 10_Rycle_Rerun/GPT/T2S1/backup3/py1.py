import os
import numpy as np
from PIL import Image
import argparse
import csv

# Core function: Get line grayscale values
def get_line_grayscale(image, start_point, end_point):
    """
    Returns grayscale values (0-255) along the line from start_point to end_point.
    """
    x0, y0 = start_point
    x1, y1 = end_point
    # Use Bresenham's line algorithm to sample points along the line
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1

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
    # Get grayscale values
    grayscale_values = []
    for (x, y) in points:
        if 0 <= x < image.width and 0 <= y < image.height:
            grayscale = image.getpixel((x, y))
            if isinstance(grayscale, tuple):  # If image is RGB, take the average
                grayscale = int(np.mean(grayscale))
            grayscale_values.append(grayscale)
        else:
            grayscale_values.append(None)  # Out of bounds
    return grayscale_values, points

# Core function: Calculate μ_eq
def calculate_μeq(grayscale_values, u_max=65535, u_min=0):
    """
    Convert grayscale (0-255) to μ_eq using linear mapping.
    """
    grayscale_np = np.array(grayscale_values, dtype=np.float32)
    # Handle None values (out of bounds) as NaN
    mask = [g is not None for g in grayscale_values]
    grayscale_np[~np.array(mask)] = np.nan
    μeq = u_min + (u_max - u_min) * (grayscale_np / 255)
    return μeq

# Plot function: Plot μ_eq curve
def plot_μeq_curve(μeq, save_path=None):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5))
    plt.plot(μeq, marker='o')
    plt.xlabel('Point Index Along Line')
    plt.ylabel('μ_eq')
    plt.title('μ_eq Curve Along Line')
    if save_path:
        plt.savefig(save_path)
    plt.show()

# Main program execution
def main():
    parser = argparse.ArgumentParser(description='Extract grayscale values along a line in an image.')
    parser.add_argument('-resolution', type=float, required=True, help='Image resolution (pixel spacing, e.g., 0.9)')
    parser.add_argument('-image_dir', type=str, required=False, default=r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png", help='Input image path')
    parser.add_argument('-output_dir', type=str, required=False, default=r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup3", help='Output directory')
    args = parser.parse_args()

    image_path = args.image_dir
    output_dir = args.output_dir
    resolution = args.resolution

    start_point = (152, 29)
    end_point = (136, 91)
    u_max = 65535
    u_min = 0

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load image
    image = Image.open(image_path).convert('L')
    print(f"Loaded image: {image_path}")
    print(f"Image size: {image.size}")

    # Get grayscale values along the line
    grayscale_values, points = get_line_grayscale(image, start_point, end_point)
    print(f"Number of points along the line: {len(grayscale_values)}")
    print(f"First 10 grayscale values: {grayscale_values[:10]}")

    # Calculate physical length of the segment
    pixel_distance = np.hypot(end_point[0] - start_point[0], end_point[1] - start_point[1])
    segment_length = pixel_distance * resolution
    print(f"Pixel distance between points: {pixel_distance:.2f}")
    print(f"Physical length of segment (in same units as resolution): {segment_length:.2f}")

    # Calculate μ_eq values
    μeq = calculate_μeq(grayscale_values, u_max, u_min)
    print(f"First 10 μ_eq values: {μeq[:10]}")

    # Save grayscale values and μ_eq to CSV
    csv_filename = f'grayscale_and_μeq_res{resolution}.csv'
    csv_path = os.path.join(output_dir, csv_filename)
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x', 'y', 'Grayscale', 'μ_eq'])
        for (pt, g, m) in zip(points, grayscale_values, μeq):
            writer.writerow([pt[0], pt[1], g, m])
    print(f"Grayscale and μ_eq values saved to: {csv_path}")

    # Optionally plot μ_eq curve
    # plot_μeq_curve(μeq)

if __name__ == "__main__":
    main()
