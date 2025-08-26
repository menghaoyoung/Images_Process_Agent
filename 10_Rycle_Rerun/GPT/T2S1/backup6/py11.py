import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys
import io
import csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Output and file path settings
output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup6"
resolution = 0.9
csv_filename = f'grayscale_line_res{resolution}.csv'
csv_path = os.path.join(output_dir, csv_filename)
mu_eq_curve_path = os.path.join(output_dir, f'mu_eq_curve_res{resolution}.png')

# Core function: Get line grayscale values
def get_line_grayscale():
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            arr = np.array([int(float(x)) for x in row])
            print("Grayscale values read from CSV:", arr)
            return arr
    return None

# Core function: Calculate u_eq
def calculate_μeq() -> np.ndarray:
    grayscale_values = get_line_grayscale()
    min_val = grayscale_values.min()
    max_val = grayscale_values.max()
    if max_val - min_val == 0:
        mu_eq = np.zeros_like(grayscale_values, dtype=float)
    else:
        mu_eq = (grayscale_values - min_val) / (max_val - min_val)
    print("μ_eq values (first 10):", mu_eq[:10])
    return mu_eq

# Plot function: Plot u_eq curve
def plot_μeq_curve():
    mu_eq = calculate_μeq()
    plt.figure(figsize=(8, 4))
    plt.plot(mu_eq, marker='o')
    plt.title(r'$\mu_{eq}$ Curve Along Line')
    plt.xlabel('Point Index')
    plt.ylabel(r'$\mu_{eq}$ (Normalized Grayscale)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(mu_eq_curve_path, dpi=150)
    print(f"μ_eq curve plot saved to: {mu_eq_curve_path}")
    plt.show()

# Main program execution
def main():
    plot_μeq_curve()

if __name__ == '__main__':
    main()
