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
    # Parameters (should match previous runs)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup8"
    image_name = "Li_1.0"
    start_point = (152, 29)
    end_point = (136, 91)
    resolution = 1.08

    # Compose CSV file name and path
    csv_filename = f"{image_name}_line_{start_point[0]}_{start_point[1]}_{end_point[0]}_{end_point[1]}_res{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_filename)

    # Ensure CSV exists
    if not os.path.exists(csv_path):
        print(f"CSV file does not exist: {csv_path}")
        return

    # Get grayscale values
    gray_values = get_line_grayscale(csv_path)

    # Print values and statistics
    print("Grayscale values loaded from CSV:")
    print(gray_values.tolist())
    print(f"Number of points: {len(gray_values)}")
    print(f"Mean grayscale: {np.mean(gray_values):.2f}")
    print(f"Std grayscale: {np.std(gray_values):.2f}")
    print(f"Min grayscale: {np.min(gray_values)}")
    print(f"Max grayscale: {np.max(gray_values)}")

    # Cumulative sum plot (additional analysis)
    plt.figure(figsize=(10, 4))
    plt.plot(np.cumsum(gray_values), marker='.', linestyle='-', color='green')
    plt.title("Cumulative Sum of Grayscale Values Along Line")
    plt.xlabel("Index Along Line")
    plt.ylabel("Cumulative Grayscale Value")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
