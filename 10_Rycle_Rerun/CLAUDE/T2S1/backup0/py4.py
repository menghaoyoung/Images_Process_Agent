# py1.py - First program to calculate and save grayscale values
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
    """
    Extract grayscale values along a line segment from start_point to end_point.
    
    Args:
        image_path: Path to the input image
        start_point: (x, y) tuple of starting point
        end_point: (x, y) tuple of ending point
        resolution: Image resolution in mm/pixel
        
    Returns:
        line_length_mm: Length of line in millimeters
        grayscale_values: List of grayscale values along the line
    """
    try:
        # Open image and convert to grayscale
        image = Image.open(image_path).convert('L')
        img_array = np.array(image)
        
        # Calculate the number of points to sample along the line
        x1, y1 = start_point
        x2, y2 = end_point
        
        # Calculate Euclidean distance in pixels
        distance_px = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        # Convert to millimeters
        line_length_mm = distance_px * resolution
        
        # Number of points to sample (at least as many as pixels in the line)
        num_points = int(distance_px) + 1
        
        # Generate points along the line
        x_values = np.linspace(x1, x2, num_points)
        y_values = np.linspace(y1, y2, num_points)
        
        # Extract grayscale values
        grayscale_values = []
        for i in range(num_points):
            x, y = int(round(x_values[i])), int(round(y_values[i]))
            # Ensure coordinates are within image bounds
            if 0 <= x < img_array.shape[1] and 0 <= y < img_array.shape[0]:
                grayscale_values.append(int(img_array[y, x]))
            else:
                print(f"Warning: Point ({x}, {y}) is outside image boundaries.")
        
        return line_length_mm, grayscale_values
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None, None

# Save grayscale values to CSV
def save_to_csv(output_path, line_length_mm, grayscale_values):
    """Save line length and grayscale values to a CSV file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Line Length (mm)', line_length_mm])
        writer.writerow(['Position', 'Grayscale Value (0-255)'])
        for i, value in enumerate(grayscale_values):
            writer.writerow([i, value])
    
    print(f"Grayscale values saved to {output_path}")

# Main program execution
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract grayscale values along a line segment.')
    parser.add_argument('-resolution', type=float, required=True, help='Image resolution in mm/pixel')
    args = parser.parse_args()
    
    # Image path and parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup"
    output_file = os.path.join(output_dir, f"grayscale_values_res_{args.resolution}.csv")
    
    # Get grayscale values
    line_length_mm, grayscale_values = get_line_grayscale(image_path, start_point, end_point, args.resolution)
    
    if line_length_mm is not None and grayscale_values:
        # Print results
        print(f"Line length: {line_length_mm:.2f} mm")
        print(f"Number of points sampled: {len(grayscale_values)}")
        print(f"Grayscale values range: {min(grayscale_values)} to {max(grayscale_values)}")
        
        # Save to CSV
        save_to_csv(output_file, line_length_mm, grayscale_values)
    else:
        print("Failed to extract grayscale values.")

if __name__ == "__main__":
    main()
