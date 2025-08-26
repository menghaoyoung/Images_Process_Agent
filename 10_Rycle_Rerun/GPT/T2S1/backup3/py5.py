import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Core function: Get line grayscale values
def get_line_grayscale(csv_path):
    """
    Reads grayscale values and coordinates from CSV.
    Returns points (list of (x,y)) and grayscale_values (list).
    """
    points = []
    grayscale_values = []
    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            x = int(float(row['x']))
            y = int(float(row['y']))
            g = None if row['Grayscale'] == '' else float(row['Grayscale'])
            points.append((x, y))
            grayscale_values.append(g)
    return points, grayscale_values

# Core function: Calculate μ_eq
def calculate_μeq(grayscale_values, u_max=65535, u_min=0):
    """
    Convert grayscale (0-255) to μ_eq using linear mapping.
    Handles None as masked (NaN).
    """
    arr = np.array(grayscale_values, dtype=np.float32)
    mask = np.isfinite(arr)
    arr[~mask] = 0
    μeq = u_min + (u_max - u_min) * (arr / 255)
    return μeq

# Plot function: Plot u_eq curve
def plot_μeq_curve(μeq, output_dir, show=False):
    plt.figure(figsize=(10, 4))
    plt.plot(μeq, marker='o', linestyle='-', color='b')
    plt.xlabel('Point Index Along Line')
    plt.ylabel('μ_eq')
    plt.title('μ_eq Curve Along Line')
    plt.grid(True)
    plot_path = os.path.join(output_dir, 'μeq_curve.png')
    plt.tight_layout()
    plt.savefig(plot_path)
    if show:
        plt.show()
    plt.close()
    print(f"μ_eq curve saved to: {plot_path}")

# Main program execution
def main():
    # File parameters (as in previous steps)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup3"
    resolution = 0.9
    csv_filename = f'grayscale_and_μeq_res{resolution}.csv'
    csv_path = os.path.join(output_dir, csv_filename)

    u_max = 65535
    u_min = 0

    # Check if CSV exists
    if not os.path.exists(csv_path):
        print("CSV file does not exist. Please run py1.py first.")
        sys.exit(1)

    # Get grayscale values from CSV
    points, grayscale_values = get_line_grayscale(csv_path)
    print(f"Loaded {len(grayscale_values)} grayscale values from CSV.")

    # Calculate μ_eq
    μeq = calculate_μeq(grayscale_values, u_max, u_min)
    print(f"First 10 μ_eq values: {μeq[:10]}")

    # Plot and save curve
    plot_μeq_curve(μeq, output_dir, show=False)

if __name__ == "__main__":
    main()
