# py1.py - The main program that processes the image
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
    # Open the image and convert to grayscale
    try:
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
        
        print(f"Image loaded successfully. Shape: {img_array.shape}")
    except Exception as e:
        print(f"Error loading image: {e}")
        return None, 0
    
    # Extract coordinates
    x1, y1 = start_point
    x2, y2 = end_point
    
    # Calculate Euclidean distance
    distance_pixels = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    distance_mm = distance_pixels * resolution
    print(f"Line length: {distance_pixels:.2f} pixels = {distance_mm:.2f} mm (at {resolution} mm/pixel)")
    
    # Generate points along the line
    num_points = int(distance_pixels) + 1
    x_values = np.linspace(x1, x2, num_points)
    y_values = np.linspace(y1, y2, num_points)
    
    # Extract grayscale values
    grayscale_values = []
    for i in range(num_points):
        x, y = int(round(x_values[i])), int(round(y_values[i]))
        # Ensure coordinates are within image bounds
        if 0 <= x < img_array.shape[1] and 0 <= y < img_array.shape[0]:
            grayscale_values.append(img_array[y, x])
        else:
            print(f"Warning: Point ({x}, {y}) is outside image boundaries")
    
    # Create output directory if it doesn't exist
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup5"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save grayscale values to CSV
    output_file = os.path.join(output_dir, f"grayscale_values_res{resolution}.csv")
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Position', 'Grayscale'])
        for i, value in enumerate(grayscale_values):
            writer.writerow([i, value])
    
    print(f"Grayscale values saved to {output_file}")
    
    return grayscale_values, distance_mm

# Main program execution
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Extract grayscale values along a line segment.')
    parser.add_argument('-resolution', type=float, required=True, help='Image resolution in mm/pixel')
    args = parser.parse_args()
    
    # Parameters
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    
    # Get grayscale values
    grayscale_values, distance_mm = get_line_grayscale(image_path, start_point, end_point, args.resolution)
    
    # Plot grayscale values
    if grayscale_values is not None:
        plt.figure(figsize=(10, 6))
        plt.plot(grayscale_values, '-o')
        plt.title(f'Grayscale Values Along Line (Length: {distance_mm:.2f} mm)')
        plt.xlabel('Position')
        plt.ylabel('Grayscale Value (0-255)')
        plt.grid(True)
        
        # Save plot
        output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup5"
        plt.savefig(os.path.join(output_dir, f"grayscale_plot_res{args.resolution}.png"))
        print(f"Plot saved to {output_dir}")

if __name__ == "__main__":
    main()
