import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import io
import argparse
import csv
from scipy.ndimage import map_coordinates
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Core function: Get line grayscale values
def get_line_grayscale(image_path, start_point, end_point, resolution):
    """
    Extract grayscale values along a line segment in an image.
    
    Args:
        image_path: Path to the input image
        start_point: (x, y) coordinates of line start
        end_point: (x, y) coordinates of line end
        resolution: Image resolution in mm per pixel
    
    Returns:
        distances: Physical distances along the line (in mm)
        grayscale_values: Grayscale values along the line
    """
    # Load the image and convert to grayscale if needed
    image = Image.open(image_path).convert('L')
    img_array = np.array(image)
    
    # Calculate the line length in pixels
    x1, y1 = start_point
    x2, y2 = end_point
    pixel_length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    # Calculate physical length in mm
    physical_length = pixel_length * resolution
    print(f"Line length: {pixel_length:.2f} pixels, {physical_length:.2f} mm")
    
    # Generate coordinates along the line
    num_points = int(pixel_length) + 1
    x_coords = np.linspace(x1, x2, num_points)
    y_coords = np.linspace(y1, y2, num_points)
    
    # Extract grayscale values along the line
    # Using map_coordinates for proper interpolation
    coords = np.vstack((y_coords, x_coords))
    grayscale_values = map_coordinates(img_array, coords, order=1)
    
    # Calculate physical distances along the line
    distances = np.linspace(0, physical_length, num_points)
    
    return distances, grayscale_values

def save_to_csv(distances, grayscale_values, output_dir, resolution):
    """Save the distances and grayscale values to a CSV file"""
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"line_grayscale_res_{resolution}.csv")
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Distance (mm)', 'Grayscale Value (0-255)'])
        for dist, val in zip(distances, grayscale_values):
            writer.writerow([dist, val])
    
    print(f"Grayscale values saved to {output_file}")
    return output_file

# Main program execution
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract grayscale values along a line segment.')
    parser.add_argument('-resolution', type=float, required=True, help='Image resolution in mm per pixel')
    args = parser.parse_args()
    
    # Define input parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup9"
    
    # Get grayscale values along the line
    distances, grayscale_values = get_line_grayscale(image_path, start_point, end_point, args.resolution)
    
    # Save results to CSV
    csv_file = save_to_csv(distances, grayscale_values, output_dir, args.resolution)
    
    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(distances, grayscale_values, 'b-')
    plt.xlabel('Distance (mm)')
    plt.ylabel('Grayscale Value (0-255)')
    plt.title(f'Grayscale Profile (Resolution: {args.resolution} mm/pixel)')
    plt.grid(True)
    
    # Save the plot
    plot_file = os.path.join(output_dir, f"line_grayscale_plot_res_{args.resolution}.png")
    plt.savefig(plot_file)
    print(f"Plot saved to {plot_file}")

if __name__ == "__main__":
    main()
