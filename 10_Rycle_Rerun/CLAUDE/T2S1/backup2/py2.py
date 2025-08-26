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
def get_line_grayscale(image_path, start_point, end_point, resolution):
    try:
        # Open the image and convert to grayscale
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
        
        # Extract coordinates
        x1, y1 = start_point
        x2, y2 = end_point
        
        # Calculate the distance between the two points
        distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        # Calculate the physical distance based on resolution (in mm)
        physical_distance_mm = distance * resolution
        
        print(f"Line segment length: {physical_distance_mm:.2f} mm")
        
        # Calculate number of points to sample along the line
        # We'll use the actual pixel distance to ensure we sample every pixel
        num_points = int(distance) + 1
        
        # Create arrays of x and y coordinates for points along the line
        x_coords = np.linspace(x1, x2, num_points).astype(int)
        y_coords = np.linspace(y1, y2, num_points).astype(int)
        
        # Extract the grayscale values along the line
        grayscale_values = img_array[y_coords, x_coords]
        
        print(f"Extracted {len(grayscale_values)} grayscale values along the line")
        
        # Create an array with position and grayscale values
        positions = np.linspace(0, physical_distance_mm, num_points)
        result_array = np.column_stack((positions, grayscale_values))
        
        return result_array, physical_distance_mm
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return None, 0

# Main program execution
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract grayscale values along a line segment.')
    parser.add_argument('-resolution', type=float, required=True, help='Image resolution in mm/pixel')
    args = parser.parse_args()
    
    # Define parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup2"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get grayscale values along the line
    grayscale_data, line_length = get_line_grayscale(image_path, start_point, end_point, args.resolution)
    
    if grayscale_data is not None:
        # Create output filename
        output_filename = f"line_grayscale_res_{args.resolution}.csv"
        output_path = os.path.join(output_dir, output_filename)
        
        # Save data to CSV file
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Position (mm)', 'Grayscale Value (0-255)'])
            writer.writerows(grayscale_data)
        
        print(f"Grayscale values saved to {output_path}")
        
        # Create a plot of the grayscale values
        plt.figure(figsize=(10, 6))
        plt.plot(grayscale_data[:, 0], grayscale_data[:, 1], '-o', markersize=3)
        plt.title(f'Grayscale Values Along Line Segment (Length: {line_length:.2f} mm)')
        plt.xlabel('Position (mm)')
        plt.ylabel('Grayscale Value')
        plt.grid(True)
        
        # Save the plot
        plot_filename = f"line_grayscale_plot_res_{args.resolution}.png"
        plot_path = os.path.join(output_dir, plot_filename)
        plt.savefig(plot_path)
        plt.close()
        
        print(f"Plot saved to {plot_path}")

if __name__ == "__main__":
    main()
