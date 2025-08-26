# py1.py - Program to calculate grayscale values along a line segment
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import io
import argparse
import csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Core function: Get line grayscale values
def get_line_grayscale(image_path, start_point, end_point, resolution):
    """
    Extract grayscale values along a line segment from an image.
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

if __name__ == "__main__":
    main()
