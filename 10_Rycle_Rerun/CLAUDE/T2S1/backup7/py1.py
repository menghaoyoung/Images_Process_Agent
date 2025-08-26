import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import io
import argparse
import csv
from math import sqrt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Core function: Get line grayscale values
def get_line_grayscale(image_path, start_point, end_point, resolution=1.0):
    """
    Extract grayscale values along a line from start_point to end_point.
    
    Args:
        image_path: Path to the image file
        start_point: (x, y) tuple for the starting point
        end_point: (x, y) tuple for the ending point
        resolution: Image resolution in mm/pixel
        
    Returns:
        List of grayscale values along the line
        Physical length of the line segment in mm
    """
    try:
        # Open and convert image to grayscale
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
        
        # Extract coordinates
        x0, y0 = start_point
        x1, y1 = end_point
        
        # Calculate pixel distance
        pixel_distance = sqrt((x1 - x0)**2 + (y1 - y0)**2)
        
        # Calculate physical distance (mm)
        physical_length = pixel_distance * resolution
        
        # Number of points to sample along the line
        num_points = int(pixel_distance) + 1
        
        # Generate points along the line
        x_points = np.linspace(x0, x1, num_points, dtype=int)
        y_points = np.linspace(y0, y1, num_points, dtype=int)
        
        # Extract grayscale values
        grayscale_values = [img_array[y, x] for x, y in zip(x_points, y_points)]
        
        print(f"Line segment length: {physical_length:.2f} mm")
        print(f"Number of sampled points: {len(grayscale_values)}")
        
        return grayscale_values, physical_length
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return [], 0

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
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup7"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get grayscale values and line length
    grayscale_values, length = get_line_grayscale(image_path, start_point, end_point, args.resolution)
    
    if grayscale_values:
        # Save to CSV file
        output_file = os.path.join(output_dir, f"line_grayscale_res_{args.resolution}.csv")
        
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Position', 'Grayscale Value (0-255)'])
            for i, value in enumerate(grayscale_values):
                writer.writerow([i, value])
        
        print(f"Grayscale values saved to: {output_file}")
        
        # Save as NumPy array
        np_output_file = os.path.join(output_dir, f"line_grayscale_res_{args.resolution}.npy")
        np.save(np_output_file, np.array(grayscale_values))
        print(f"Grayscale values also saved as NumPy array to: {np_output_file}")
        
        # Create a plot of the grayscale values
        plt.figure(figsize=(10, 6))
        plt.plot(grayscale_values)
        plt.title(f'Grayscale Values Along Line Segment (Length: {length:.2f} mm)')
        plt.xlabel('Position')
        plt.ylabel('Grayscale Value (0-255)')
        plt.grid(True)
        
        # Save the plot
        plot_file = os.path.join(output_dir, f"line_grayscale_plot_res_{args.resolution}.png")
        plt.savefig(plot_file)
        print(f"Plot saved to: {plot_file}")

if __name__ == "__main__":
    main()
