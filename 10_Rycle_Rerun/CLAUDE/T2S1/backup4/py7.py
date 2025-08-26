# py1.py - Program to calculate grayscale values along a line
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import io
import argparse
import csv
from scipy.ndimage import map_coordinates
import math

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Core function: Get line grayscale values
def get_line_grayscale(image_path, start_point, end_point, resolution):
    # Load the image
    try:
        img = Image.open(image_path)
        img_gray = img.convert('L')  # Convert to grayscale
        img_array = np.array(img_gray)
        
        print(f"Image loaded successfully. Shape: {img_array.shape}")
    except Exception as e:
        print(f"Error loading image: {e}")
        return None, 0
    
    # Calculate the physical length of the line in mm
    x1, y1 = start_point
    x2, y2 = end_point
    
    # Calculate the number of pixels in the line
    pixel_distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    # Calculate the physical length in mm
    physical_length = pixel_distance * resolution
    print(f"Line physical length: {physical_length:.2f} mm")
    
    # Create coordinates for line sampling
    num_points = int(pixel_distance) + 1
    x_coords = np.linspace(start_point[0], end_point[0], num_points)
    y_coords = np.linspace(start_point[1], end_point[1], num_points)
    
    # Sample the image along the line
    coords = np.vstack((y_coords, x_coords))
    grayscale_values = map_coordinates(img_array, coords, order=1)
    
    # Create array with positions and grayscale values
    result = np.zeros((len(grayscale_values), 4))
    for i in range(len(grayscale_values)):
        # Calculate the relative position along the line (0 to 1)
        position = i / (num_points - 1)
        # Calculate the actual physical position in mm
        physical_position = position * physical_length
        
        result[i, 0] = x_coords[i]  # x-coordinate
        result[i, 1] = y_coords[i]  # y-coordinate
        result[i, 2] = physical_position  # position in mm
        result[i, 3] = grayscale_values[i]  # grayscale value
    
    return result, physical_length

# Main program execution
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Calculate grayscale values along a line segment.')
    parser.add_argument('-resolution', type=float, required=True, help='Image resolution in mm/pixel')
    args = parser.parse_args()
    
    # Fixed parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup4"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the grayscale values along the line
    line_data, physical_length = get_line_grayscale(image_path, start_point, end_point, args.resolution)
    
    if line_data is not None:
        # Save the data to a CSV file
        output_file = os.path.join(output_dir, f"line_grayscale_res_{args.resolution}.csv")
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['X', 'Y', 'Position (mm)', 'Grayscale Value'])
            writer.writerows(line_data)
        
        print(f"Grayscale values saved to: {output_file}")
        print(f"Total points: {len(line_data)}")
        print(f"Line physical length: {physical_length:.2f} mm")
        
        # Also save just the grayscale values as a single column
        grayscale_only_file = os.path.join(output_dir, f"grayscale_only_res_{args.resolution}.csv")
        with open(grayscale_only_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Grayscale Value'])
            for row in line_data:
                writer.writerow([row[3]])
        
        print(f"Grayscale values only saved to: {grayscale_only_file}")
        
        # Plot the grayscale profile
        plt.figure(figsize=(10, 6))
        plt.plot(line_data[:, 2], line_data[:, 3], 'b-')
        plt.xlabel('Position (mm)')
        plt.ylabel('Grayscale Value')
        plt.title(f'Grayscale Profile (Resolution: {args.resolution} mm/pixel)')
        plt.grid(True)
        
        # Save the plot
        plot_file = os.path.join(output_dir, f"grayscale_plot_res_{args.resolution}.png")
        plt.savefig(plot_file)
        print(f"Grayscale plot saved to: {plot_file}")

if __name__ == "__main__":
    main()
