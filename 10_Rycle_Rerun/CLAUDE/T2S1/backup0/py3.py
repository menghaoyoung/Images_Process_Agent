# py1.py - Program to extract grayscale values along a line in an image
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import io
import argparse
import csv
from pathlib import Path
import math

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Core function: Get line grayscale values
def get_line_grayscale(image_path, start_point, end_point, resolution):
    """
    Extract grayscale values along a line segment in an image.
    
    Args:
        image_path: Path to the input image
        start_point: Starting point (x, y) of the line
        end_point: Ending point (x, y) of the line
        resolution: Image resolution in mm/pixel
        
    Returns:
        tuple: (grayscale_values, line_length_mm)
    """
    try:
        # Open and convert image to grayscale
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
        
        # Extract coordinates
        x1, y1 = start_point
        x2, y2 = end_point
        
        # Calculate Euclidean distance in pixels
        pixel_distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        # Convert to mm using resolution
        line_length_mm = pixel_distance * resolution
        
        # Calculate the number of points to sample along the line
        # Use the pixel distance to ensure we sample each pixel along the line
        num_points = int(pixel_distance) + 1
        
        # Generate points along the line
        x_values = np.linspace(x1, x2, num_points)
        y_values = np.linspace(y1, y2, num_points)
        
        # Extract grayscale values at each point
        grayscale_values = []
        for i in range(num_points):
            x, y = int(round(x_values[i])), int(round(y_values[i]))
            # Ensure we're within image boundaries
            if 0 <= x < img_array.shape[1] and 0 <= y < img_array.shape[0]:
                grayscale_values.append(img_array[y, x])
            else:
                print(f"Warning: Point ({x}, {y}) is outside image boundaries")
                grayscale_values.append(0)  # Append 0 for out-of-bounds points
        
        print(f"Extracted {len(grayscale_values)} grayscale values along the line")
        print(f"Line length: {line_length_mm:.2f} mm")
        
        return grayscale_values, line_length_mm
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return [], 0

# Main program execution
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract grayscale values along a line in an image')
    parser.add_argument('-resolution', type=float, required=True, help='Image resolution in mm/pixel')
    args = parser.parse_args()
    
    # Set parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    resolution = args.resolution
    
    # Output directory
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup1"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get grayscale values and line length
    grayscale_values, line_length = get_line_grayscale(image_path, start_point, end_point, resolution)
    
    if grayscale_values:
        # Create output CSV file
        output_file = os.path.join(output_dir, f"line_grayscale_res_{resolution}.csv")
        
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Index', 'Grayscale Value (0-255)'])
            for i, value in enumerate(grayscale_values):
                writer.writerow([i, value])
        
        print(f"Grayscale values saved to: {output_file}")
        
        # Plot the grayscale values
        plt.figure(figsize=(10, 6))
        plt.plot(grayscale_values, '-o', markersize=3)
        plt.title(f'Grayscale Values Along Line (Length: {line_length:.2f} mm)')
        plt.xlabel('Position along line (pixel index)')
        plt.ylabel('Grayscale Value (0-255)')
        plt.grid(True)
        
        # Save the plot
        plot_file = os.path.join(output_dir, f"line_grayscale_plot_res_{resolution}.png")
        plt.savefig(plot_file)
        print(f"Plot saved to: {plot_file}")
        
        # Also save the line length to a separate file
        length_file = os.path.join(output_dir, f"line_length_res_{resolution}.txt")
        with open(length_file, 'w') as f:
            f.write(f"Line length: {line_length:.2f} mm\n")
            f.write(f"Start point: {start_point}\n")
            f.write(f"End point: {end_point}\n")
            f.write(f"Resolution: {resolution} mm/pixel\n")
        
        print(f"Line length information saved to: {length_file}")

if __name__ == "__main__":
    main()
