import os
import numpy as np
import matplotlib.pyplot as plt
import sys
import io
import csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Core function: Get line grayscale values from CSV
def get_line_grayscale(csv_path):
    """
    Reads grayscale values from the specified CSV file and returns them as a numpy array.
    """
    gray_values = []
    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            gray_values.append(int(row['Grayscale']))
    return np.array(gray_values)

# Main program execution
def main():
    # Parameters must match those used in previous steps
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup8"
    image_name = "Li_1.0"
    start_point = (152, 29)
    end_point = (136, 91)
    resolution = 1.08

    # Build expected CSV file name
    csv_filename = f"{image_name}_line_{start_point[0]}_{start_point[1]}_{end_point[0]}_{end_point[1]}_res{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_filename)

    # Check if the CSV file exists
    if not os.path.exists(csv_path):
        print(f"CSV file does not exist: {csv_path}")
        return

    # Get grayscale values
    gray_values = get_line_grayscale(csv_path)
    print("Grayscale values loaded from CSV:")
    print(gray_values.tolist())

    # Compute and print statistics
    print(f"Number of points: {len(gray_values)}")
    print(f"Mean grayscale: {np.mean(gray_values):.2f}")
    print(f"Std grayscale: {np.std(gray_values):.2f}")
    print(f"Min grayscale: {np.min(gray_values)}")
    print(f"Max grayscale: {np.max(gray_values)}")

    # Optional: Histogram
    plt.figure(figsize=(8,4))
    plt.hist(gray_values, bins=range(0, 257, 8), color='gray', edgecolor='black')
    plt.title("Histogram of Grayscale Values Along the Line")
    plt.xlabel("Grayscale Value")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
