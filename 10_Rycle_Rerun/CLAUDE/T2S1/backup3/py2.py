# py1.py - Program to calculate grayscale values along a line segment
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import io
import argparse
import csv
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Core function: Get line grayscale values
def get_line_grayscale(image_path, start_point, end_point, resolution):
    """
    Extract grayscale values along a line segment from an image.
    
    Args:
        image_path: Path to the image file
        start_point: Tuple (x, y) for the starting point of the line
        end_point: Tuple (x, y) for the ending point of the line
        resolution: Pixel resolution in mm/pixel
        
    Returns:
        Dictionary containing:
        - grayscale_values: List of grayscale values along the line
        - physical_length: Physical length of the line segment in mm
        - pixel_length: Length of the line segment in pixels
    """
    try:
        # Open the image and convert to grayscale
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
        
        # Extract coordinates
        x0, y0 = start_point
        x1, y1 = end_point
        
        # Calculate pixel distance using Euclidean distance
        pixel_length = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
        
        # Calculate physical length in mm
        physical_length = pixel_length * resolution
        
        # Calculate number of points to sample along the line
        # We'll sample at least as many points as pixels in the line
        num_points = int(np.ceil(pixel_length)) + 1
        
        # Generate evenly spaced points along the line
        x_points = np.linspace(x0, x1, num_points)
        y_points = np.linspace(y0, y1, num_points)
        
        # Extract grayscale values at each point
        grayscale_values = []
        for i in range(num_points):
            x, y = int(round(x_points[i])), int(round(y_points[i]))
            # Ensure coordinates are within image bounds
            if 0 <= x < img_array.shape[1] and 0 <= y < img_array.shape[0]:
                grayscale_values.append(int(img_array[y, x]))
            else:
                grayscale_values.append(None)  # Out of bounds
        
        return {
            "grayscale_values": grayscale_values,
            "physical_length": physical_length,
            "pixel_length": pixel_length
        }
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# Main program execution
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract grayscale values along a line segment.')
    parser.add_argument('-resolution', type=float, required=True, help='Pixel resolution in mm/pixel')
    args = parser.parse_args()
    
    # Define parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    resolution = args.resolution
    
    # Output directory
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup3"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get grayscale values
    result = get_line_grayscale(image_path, start_point, end_point, resolution)
    
    if result:
        # Print results
        print(f"Line segment from {start_point} to {end_point}:")
        print(f"Pixel length: {result['pixel_length']:.2f} pixels")
        print(f"Physical length: {result['physical_length']:.2f} mm")
        print(f"Number of grayscale values: {len(result['grayscale_values'])}")
        
        # Save grayscale values to CSV
        csv_filename = os.path.join(output_dir, f"grayscale_values_res_{resolution}.csv")
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Index', 'Grayscale Value'])
            for i, value in enumerate(result['grayscale_values']):
                writer.writerow([i, value])
        
        print(f"Grayscale values saved to {csv_filename}")
        
        # Save results summary
        summary_filename = os.path.join(output_dir, f"line_summary_res_{resolution}.txt")
        with open(summary_filename, 'w') as f:
            f.write(f"Line segment from {start_point} to {end_point}\n")
            f.write(f"Image: {image_path}\n")
            f.write(f"Resolution: {resolution} mm/pixel\n")
            f.write(f"Pixel length: {result['pixel_length']:.2f} pixels\n")
            f.write(f"Physical length: {result['physical_length']:.2f} mm\n")
            f.write(f"Number of grayscale values: {len(result['grayscale_values'])}\n")
        
        print(f"Summary saved to {summary_filename}")
        
        # Optional: Plot the grayscale values
        plt.figure(figsize=(10, 6))
        plt.plot(result['grayscale_values'])
        plt.title(f'Grayscale Values Along Line (Resolution: {resolution} mm/pixel)')
        plt.xlabel('Position along line (pixel index)')
        plt.ylabel('Grayscale Value (0-255)')
        plt.grid(True)
        
        # Save the plot
        plot_filename = os.path.join(output_dir, f"grayscale_plot_res_{resolution}.png")
        plt.savefig(plot_filename)
        print(f"Plot saved to {plot_filename}")

if __name__ == "__main__":
    main()
