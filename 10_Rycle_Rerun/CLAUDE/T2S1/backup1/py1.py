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
    # Open the image and convert to grayscale
    try:
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
        print(f"Image loaded successfully with shape: {img_array.shape}")
    except Exception as e:
        print(f"Error loading image: {e}")
        return None
    
    # Calculate the physical length of the line (in mm)
    # resolution is in mm/pixel
    x1, y1 = start_point
    x2, y2 = end_point
    pixel_distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    physical_length = pixel_distance * resolution
    
    # Get the grayscale values along the line
    # Number of points to sample along the line
    num_points = int(pixel_distance) + 1
    
    # Generate points along the line
    x_points = np.linspace(x1, x2, num_points)
    y_points = np.linspace(y1, y2, num_points)
    
    # Extract grayscale values
    grayscale_values = []
    for i in range(num_points):
        x, y = int(round(x_points[i])), int(round(y_points[i]))
        # Ensure we're within image boundaries
        if 0 <= x < img_array.shape[1] and 0 <= y < img_array.shape[0]:
            grayscale_values.append(img_array[y, x])
        else:
            print(f"Warning: Point ({x}, {y}) is outside image boundaries")
    
    # Create output data with position information
    positions = np.linspace(0, physical_length, num_points)
    result = {
        'position_mm': positions,
        'grayscale_value': grayscale_values,
        'x_pixel': x_points,
        'y_pixel': y_points
    }
    
    return result, physical_length

# Main program execution
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract grayscale values along a line segment')
    parser.add_argument('-resolution', type=float, required=True, help='Image resolution in mm/pixel')
    args = parser.parse_args()
    
    # Define parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    resolution = args.resolution
    
    # Create output directory if it doesn't exist
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup1"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get grayscale values
    result, physical_length = get_line_grayscale(image_path, start_point, end_point, resolution)
    
    if result:
        # Save results to CSV
        output_file = os.path.join(output_dir, f"grayscale_values_res_{resolution:.2f}.csv")
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Position (mm)', 'Grayscale Value', 'X (pixel)', 'Y (pixel)'])
            for i in range(len(result['position_mm'])):
                writer.writerow([
                    result['position_mm'][i],
                    result['grayscale_value'][i],
                    result['x_pixel'][i],
                    result['y_pixel'][i]
                ])
        
        # Also save the grayscale values as a numpy array
        np_output_file = os.path.join(output_dir, f"grayscale_array_res_{resolution:.2f}.csv")
        np.savetxt(np_output_file, result['grayscale_value'], delimiter=',')
        
        print(f"Line length: {physical_length:.2f} mm")
        print(f"Number of points sampled: {len(result['grayscale_value'])}")
        print(f"Results saved to: {output_file}")
        print(f"Grayscale array saved to: {np_output_file}")
        
        # Plot the grayscale profile
        plt.figure(figsize=(10, 6))
        plt.plot(result['position_mm'], result['grayscale_value'], '-o')
        plt.title(f'Grayscale Profile (Resolution: {resolution} mm/pixel)')
        plt.xlabel('Position (mm)')
        plt.ylabel('Grayscale Value (0-255)')
        plt.grid(True)
        plot_file = os.path.join(output_dir, f"grayscale_plot_res_{resolution:.2f}.png")
        plt.savefig(plot_file)
        print(f"Plot saved to: {plot_file}")

if __name__ == "__main__":
    main()
