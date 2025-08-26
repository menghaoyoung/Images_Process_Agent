import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import io
import csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Core function: Get line grayscale values from CSV
def get_line_grayscale(csv_path):
    """
    Reads the grayscale values from the specified CSV file.
    Returns the list of grayscale values.
    """
    gray_values = []
    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            gray_values.append(int(row['Grayscale']))
    return gray_values

# Main program execution
def main():
    # Parameters (should match previous step)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup8"
    image_name = "Li_1.0"
    start_point = (152, 29)
    end_point = (136, 91)
    resolution = 1.08

    # Build CSV file path
    csv_filename = f"{image_name}_line_{start_point[0]}_{start_point[1]}_{end_point[0]}_{end_point[1]}_res{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_filename)

    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"CSV file does not exist: {csv_path}")
        return

    # Read grayscale values
    gray_values = get_line_grayscale(csv_path)
    print("Loaded grayscale values from CSV:")
    print(gray_values)

    # Plot grayscale values along the line
    plt.figure(figsize=(10, 4))
    plt.plot(gray_values, marker='o')
    plt.title(f"Grayscale values along line ({start_point})-({end_point})")
    plt.xlabel('Point index along line')
    plt.ylabel('Grayscale (0-255)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
