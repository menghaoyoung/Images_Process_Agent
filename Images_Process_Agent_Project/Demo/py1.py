import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import io
import csv
import argparse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Core function: Get line grayscale values 
def get_line_grayscale(image_path, start_point, end_point):
    # Open the image
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img_array = np.array(img)
    
    # Calculate points along the line using Bresenham's algorithm
    x0, y0 = start_point
    x1, y1 = end_point
    
    # Calculate the number of points based on distance
    distance = int(np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2))
    
    # Generate points along the line
    x_points = np.linspace(x0, x1, distance, dtype=int)
    y_points = np.linspace(y0, y1, distance, dtype=int)
    
    # Extract grayscale values
    grayscale_values = img_array[y_points, x_points]
    
    return grayscale_values, distance

# Core function: Calculate u_eq
def calculate_μeq(grayscale_values, u_min, u_max) -> np.ndarray:
    # Calculate u_eq using the formula: u_eq = u_min + (gray_values / 255) * u_max
    u_eq = u_min + (grayscale_values / 255) * u_max
    return u_eq

# Plot function: Plot u_eq curve
def plot_μeq_curve(distances, u_eq_values, output_path, filename_base):
    plt.figure(figsize=(10, 6))
    plt.plot(distances, u_eq_values, 'b-', linewidth=2)
    plt.xlabel('Distance (μm)')
    plt.ylabel('u_eq')
    plt.title('u_eq vs Distance')
    plt.grid(True)
    
    # Save as TIFF
    plot_path = os.path.join(output_path, f"{filename_base}_u_eq_plot.tiff")
    plt.savefig(plot_path, format='tiff', dpi=300)
    plt.close()
    
    print(f"Plot saved to {plot_path}")

# Main program execution
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Process image and calculate u_eq')
    parser.add_argument('-resolution', type=float, default=1.08, help='Image resolution in μm/pixel')
    args = parser.parse_args()
    
    # Parameters
    start_point = (152, 29)
    end_point = (135, 92)
    u_max = 65535
    u_min = 0
    resolution = args.resolution
    
    # Input image path
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    
    # Output directory
    output_dir = r"C:\Users\admin\Desktop\For git\All_Outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get base filename without extension
    filename_base = Path(image_path).stem
    
    # Get grayscale values along the line
    grayscale_values, pixel_distance = get_line_grayscale(image_path, start_point, end_point)
    
    # Calculate physical distance in μm
    physical_distance = pixel_distance * resolution
    
    # Save grayscale values to CSV
    grayscale_csv_path = os.path.join(output_dir, f"{filename_base}_grayscale_values.csv")
    with open(grayscale_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Position', 'Grayscale Value'])
        for i, value in enumerate(grayscale_values):
            writer.writerow([i, value])
    print(f"Grayscale values saved to {grayscale_csv_path}")
    
    # Save line segment length to text file
    length_txt_path = os.path.join(output_dir, f"{filename_base}_line_length.txt")
    with open(length_txt_path, 'w') as txtfile:
        txtfile.write(f"Line segment length: {physical_distance} μm\n")
        txtfile.write(f"Start point: {start_point}\n")
        txtfile.write(f"End point: {end_point}\n")
        txtfile.write(f"Resolution: {resolution} μm/pixel\n")
    print(f"Line segment length saved to {length_txt_path}")
    
    # Calculate u_eq values
    u_eq_values = calculate_μeq(grayscale_values, u_min, u_max)
    
    # Create distance array in μm
    distances = np.linspace(0, physical_distance, len(grayscale_values))
    
    # Save u_eq values and distances to CSV
    u_eq_csv_path = os.path.join(output_dir, f"{filename_base}_u_eq_values.csv")
    with open(u_eq_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Distance (μm)', 'u_eq'])
        for d, u in zip(distances, u_eq_values):
            writer.writerow([d, u])
    print(f"u_eq values saved to {u_eq_csv_path}")
    
    # Plot u_eq curve
    plot_μeq_curve(distances, u_eq_values, output_dir, filename_base)

if __name__ == "__main__":
    main()
