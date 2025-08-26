import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import io
import argparse
import csv
from pathlib import Path
from math import sqrt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Core function: Get line grayscale values
def get_line_grayscale(image_path, start_point, end_point, resolution=1.0):
    """
    Extract grayscale values along a line segment in an image.
    
    Args:
        image_path: Path to the input image
        start_point: Tuple (x, y) for the starting point of the line
        end_point: Tuple (x, y) for the ending point of the line
        resolution: Image resolution in mm/pixel
        
    Returns:
        tuple: (line_length_mm, grayscale_values)
    """
    try:
        # Open the image and convert to grayscale
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
        
        # Calculate pixel distance
        pixel_distance = sqrt((end_point[0] - start_point[0])**2 + 
                             (end_point[1] - start_point[1])**2)
        
        # Calculate physical distance in mm
        physical_distance_mm = pixel_distance * resolution
        
        # Generate points along the line
        num_points = int(pixel_distance) + 1
        x_values = np.linspace(start_point[0], end_point[0], num_points)
        y_values = np.linspace(start_point[1], end_point[1], num_points)
        
        # Extract grayscale values
        grayscale_values = []
        for i in range(num_points):
            x, y = int(round(x_values[i])), int(round(y_values[i]))
            # Ensure coordinates are within image bounds
            if 0 <= x < img_array.shape[1] and 0 <= y < img_array.shape[0]:
                grayscale_values.append(int(img_array[y, x]))
            else:
                print(f"Warning: Point ({x}, {y}) is outside the image boundaries.")
        
        return physical_distance_mm, grayscale_values
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return None, None

# Main program execution
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract grayscale values along a line segment.')
    parser.add_argument('-resolution', type=float, default=1.0,
                        help='Image resolution in mm/pixel')
    args = parser.parse_args()
    
    # Set parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup6"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get grayscale values
    line_length_mm, grayscale_values = get_line_grayscale(
        image_path, start_point, end_point, args.resolution)
    
    if grayscale_values:
        # Create output filename based on resolution
        output_file = os.path.join(output_dir, f"line_grayscale_res_{args.resolution}.csv")
        
        # Save results to CSV
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Index', 'Grayscale Value (0-255)'])
            for i, value in enumerate(grayscale_values):
                writer.writerow([i, value])
        
        # Print results
        print(f"Line length: {line_length_mm:.2f} mm")
        print(f"Number of points: {len(grayscale_values)}")
        print(f"Grayscale values saved to: {output_file}")
        
        # Optionally, create a plot of the grayscale values
        plt.figure(figsize=(10, 6))
        plt.plot(grayscale_values, '-o')
        plt.title(f'Grayscale Values Along Line (Resolution: {args.resolution} mm/pixel)')
        plt.xlabel('Point Index')
        plt.ylabel('Grayscale Value (0-255)')
        plt.grid(True)
        plot_file = os.path.join(output_dir, f"line_grayscale_plot_res_{args.resolution}.png")
        plt.savefig(plot_file)
        print(f"Plot saved to: {plot_file}")
        
        # Save the grayscale values as a NumPy array
        np_file = os.path.join(output_dir, f"line_grayscale_array_res_{args.resolution}.npy")
        np.save(np_file, np.array(grayscale_values))
        print(f"NumPy array saved to: {np_file}")
    else:
        print("Failed to extract grayscale values.")

if __name__ == "__main__":
    main()
