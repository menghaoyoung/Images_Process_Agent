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
    Reads grayscale values from the produced CSV file.
    Returns two arrays: indices, grayscale_values.
    """
    indices = []
    grayscale_values = []
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        for row in reader:
            indices.append(int(row[0]))
            grayscale_values.append(int(row[1]))
    return np.array(indices), np.array(grayscale_values)

# Core function: Calculate μ_eq (mm positions along the line)
def calculate_μeq(line_length_mm, num_points):
    """
    Returns an array of length (num_points) giving the physical position (in mm)
    along the line for each grayscale value (equally spaced).
    """
    if num_points <= 1:
        return np.array([0])
    # Evenly spaced positions from 0 to line_length_mm
    return np.linspace(0, line_length_mm, num_points)

# Plot function: Plot u_eq curve
def plot_μeq_curve(positions_mm, grayscale_values, output_dir):
    """
    Plots grayscale value vs. position (mm) and saves the plot.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(positions_mm, grayscale_values, marker='o', linestyle='-', color='blue')
    plt.xlabel('Position along line (mm)')
    plt.ylabel('Grayscale Value (0-255)')
    plt.title('Grayscale Profile Along Line Segment')
    plt.grid(True)
    plt.tight_layout()
    output_path = os.path.join(output_dir, "grayscale_profile_curve.png")
    plt.savefig(output_path)
    print(f"Grayscale profile curve saved to: {output_path}")
    plt.close()

# Main program execution
def main():
    # Output path setup
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup1"
    csv_path = os.path.join(output_dir, "line_grayscale_values.csv")
    len_path = os.path.join(output_dir, "line_length_mm.txt")

    # Check CSV and length files
    if not os.path.isfile(csv_path):
        print(f"CSV file not found: {csv_path}")
        return
    if not os.path.isfile(len_path):
        print(f"Line length file not found: {len_path}")
        return

    # Read grayscale values
    indices, grayscale_values = get_line_grayscale(csv_path)
    print(f"Loaded {len(grayscale_values)} grayscale values from CSV.")

    # Read line length in mm
    with open(len_path, 'r') as f:
        line = f.readline()
        # Line is of the form "Line length (mm): 57.628000"
        line_length_mm = float(line.strip().split(":")[1])

    print(f"Line length (mm): {line_length_mm}")

    # Compute positions along the line
    positions_mm = calculate_μeq(line_length_mm, len(grayscale_values))

    # Plot and save the curve
    plot_μeq_curve(positions_mm, grayscale_values, output_dir)

    # Print a few sample points
    print("Sample (position_mm, grayscale):")
    for i in range(min(10, len(grayscale_values))):
        print(f"{positions_mm[i]:.2f} mm: {grayscale_values[i]}")

if __name__ == "__main__":
    main()
