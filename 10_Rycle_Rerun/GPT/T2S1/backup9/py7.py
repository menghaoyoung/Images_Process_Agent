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
    grays = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            grays.append(int(row['grayscale']))
    return np.array(grays)

# Main program execution
def main():
    # Configuration
    resolution = 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup9"
    csv_filename = f'line_grayscale_values_res{resolution:.2f}.csv'
    csv_path = os.path.join(output_dir, csv_filename)

    # Check for CSV file existence
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found: {csv_path}")
        sys.exit(1)

    # Load grayscale values
    grayscale_values = get_line_grayscale(csv_path)
    print(f"Loaded {len(grayscale_values)} grayscale values from {csv_path}")

    # Output statistics
    print(f"Min grayscale: {np.min(grayscale_values)}")
    print(f"Max grayscale: {np.max(grayscale_values)}")
    print(f"Mean grayscale: {np.mean(grayscale_values):.2f}")

    # Plot grayscale profile
    plt.figure(figsize=(8, 4))
    plt.plot(grayscale_values, marker='o')
    plt.title(f"Grayscale Profile Along Line (resolution={resolution} mm/pixel)")
    plt.xlabel("Index Along Line")
    plt.ylabel("Grayscale Value (0-255)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
