import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import io
import argparse
import csv
from pathlib import Path
from scipy.ndimage import map_coordinates

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Core function: Get line grayscale values
def get_line_grayscale(image_path, start_point, end_point, resolution=1.0):
    """
    Extract grayscale values along a line segment in an image.
    
    Args:
        image_path: Path to the input image
        start_point: Starting point (x, y) of the line segment
        end_point: Ending point (x, y) of the line segment
        resolution: Image resolution in mm/pixel
        
    Returns:
        tuple: (grayscale_values, physical_length)
    """
    try:
        # Load the image and convert to grayscale
        image = Image.open(image_path).convert('L')
        img_array = np.array(image)
        
        # Calculate number of points along the line
        x0, y0 = start_point
        x1, y1 = end_point
        
        # Calculate Euclidean distance in pixels
        pixel_distance = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        
        # Calculate physical length in mm
        physical_length = pixel_distance * resolution
        
        # Generate points along the line
        num_points = int(pixel_distance) + 1
        x_coords = np.linspace(x0, x1, num_points)
        y_coords = np.linspace(y0, y1, num_points)
        
        # Extract grayscale values using interpolation
        coords = np.vstack((y_coords, x_coords))
        grayscale_values = map_coordinates(img_array, coords, order=1)
        
        print(f"Line segment length: {physical_length:.2f} mm")
        print(f"Number of points sampled: {num_points}")
        
        return grayscale_values, physical_length
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None, 0

# Main program execution
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract grayscale values along a line segment')
    parser.add_argument('-resolution', type=float, default=1.0, help='Image resolution in mm/pixel')
    args = parser.parse_args()
    
    # Define parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup8"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get grayscale values and length
    grayscale_values, length = get_line_grayscale(image_path, start_point, end_point, args.resolution)
    
    if grayscale_values is not None:
        # Create output file name
        resolution_str = str(args.resolution).replace('.', '_')
        output_file = os.path.join(output_dir, f"line_grayscale_res{resolution_str}.csv")
        
        # Save grayscale values to CSV
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Index', 'Grayscale Value (0-255)'])
            for i, value in enumerate(grayscale_values):
                writer.writerow([i, value])
        
        print(f"Grayscale values saved to: {output_file}")
        
        # Also save as numpy array
        np_output_file = os.path.join(output_dir, f"line_grayscale_res{resolution_str}.npy")
        np.save(np_output_file, grayscale_values)
        print(f"Grayscale values saved as numpy array to: {np_output_file}")
        
        # Plot grayscale values
        plt.figure(figsize=(10, 6))
        plt.plot(grayscale_values)
        plt.title(f'Grayscale Values Along Line (Resolution: {args.resolution} mm/pixel)')
        plt.xlabel('Position Along Line')
        plt.ylabel('Grayscale Value (0-255)')
        plt.grid(True)
        
        # Save plot
        plot_file = os.path.join(output_dir, f"line_grayscale_plot_res{resolution_str}.png")
        plt.savefig(plot_file)
        print(f"Plot saved to: {plot_file}")

if __name__ == "__main__":
    main()
