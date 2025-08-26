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
    # Parameters (should match previous steps)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup8"
    image_name = "Li_1.0"
    start_point = (152, 29)
    end_point = (136, 91)
    resolution = 1.08

    # Build CSV file path
    csv_filename = f"{image_name}_line_{start_point[0]}_{start_point[1]}_{end_point[0]}_{end_point[1]}_res{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_filename)

    # Ensure the CSV exists
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

    # Calculate first and second derivatives
    derivative = np.diff(gray_values)
    second_derivative = np.diff(derivative)

    # Local maxima and minima (from previous output)
    local_maxima = [(4, 208), (21, 89), (36, 253), (57, 185)]
    local_minima = [(14, 21), (26, 75), (49, 149)]

    # Print for clarity
    print("Local maxima (index, value):", local_maxima)
    print("Local minima (index, value):", local_minima)

    # Save analyzed results to a new CSV
    analyzed_csv = os.path.join(output_dir, f"{image_name}_line_{start_point[0]}_{start_point[1]}_{end_point[0]}_{end_point[1]}_res{resolution:.2f}_analyzed.csv")
    with open(analyzed_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Index', 'Grayscale', 'FirstDerivative', 'SecondDerivative', 'IsLocalMax', 'IsLocalMin'])
        for i in range(len(gray_values)):
            first = derivative[i] if i < len(derivative) else ''
            second = second_derivative[i] if i < len(second_derivative) else ''
            is_max = 1 if any(i == idx for idx, val in local_maxima) else 0
            is_min = 1 if any(i == idx for idx, val in local_minima) else 0
            writer.writerow([i, gray_values[i], first, second, is_max, is_min])
    print(f"Analyzed CSV saved to: {analyzed_csv}")

    # Plot with maxima/minima as before
    plt.figure(figsize=(12, 6))
    plt.plot(gray_values, marker='o', linestyle='-', label='Grayscale')
    if local_maxima:
        max_idx, max_vals = zip(*local_maxima)
        plt.scatter(max_idx, max_vals, color='red', label='Local Maxima', zorder=5)
    if local_minima:
        min_idx, min_vals = zip(*local_minima)
        plt.scatter(min_idx, min_vals, color='blue', label='Local Minima', zorder=5)
    plt.title("Grayscale Values and Local Extrema Along Line")
    plt.xlabel("Index Along Line")
    plt.ylabel("Grayscale (0-255)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
