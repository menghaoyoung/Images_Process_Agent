import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Core function: Get line grayscale values from CSV
def get_line_grayscale(csv_path):
    positions = []
    grays = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            x = int(row['x'])
            y = int(row['y'])
            gray = int(row['grayscale'])
            positions.append((x, y))
            grays.append(gray)
    return positions, grays

# Main program execution
def main():
    # Output file path and resolution settings
    resolution = 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup9"
    csv_filename = f'line_grayscale_values_res{resolution:.2f}.csv'
    csv_path = os.path.join(output_dir, csv_filename)

    # Check if file exists
    if not os.path.exists(csv_path):
        print(f"CSV file does not exist: {csv_path}")
        sys.exit(1)

    # Load grayscale values
    positions, grays = get_line_grayscale(csv_path)
    print(f"Loaded {len(grays)} grayscale values from CSV.")

    # Plot grayscale profile along the line
    plt.figure(figsize=(8, 4))
    plt.plot(range(len(grays)), grays, marker='o', linestyle='-')
    plt.title(f"Grayscale Profile Along Line (resolution={resolution} mm/pixel)")
    plt.xlabel("Point Index Along Line")
    plt.ylabel("Grayscale Value (0-255)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
