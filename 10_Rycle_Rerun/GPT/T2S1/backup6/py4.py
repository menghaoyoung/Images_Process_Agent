import os
import numpy as np
import matplotlib.pyplot as plt
import sys
import io
import csv

# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- Parameters ---
output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup6"
resolution = 0.9
csv_filename = f'grayscale_line_res{resolution}.csv'
csv_path = os.path.join(output_dir, csv_filename)

start_point = (152, 29)
end_point = (136, 91)
u_max = 65535
u_min = 0

# Core function: Get line grayscale values
def get_line_grayscale(csv_file):
    """Read grayscale values from CSV file."""
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # Flat array of grayscale values
            arr = np.array([int(float(x)) for x in row])
            return arr
    return None

# Core function: Calculate μ_eq (example: normalized grayscale)
def calculate_μeq(gray_arr) -> np.ndarray:
    """
    Example μ_eq calculation: Normalize grayscale values to [0, 1]
    More complex processing can be inserted here if needed.
    """
    mu_eq = (gray_arr - gray_arr.min()) / (gray_arr.max() - gray_arr.min() + 1e-9)
    return mu_eq

# Plot function: Plot μ_eq curve
def plot_μeq_curve(mu_eq_arr):
    plt.figure(figsize=(8,4))
    plt.plot(mu_eq_arr, marker='o')
    plt.title(r'$\mu_{eq}$ Curve Along Line')
    plt.xlabel('Point Index')
    plt.ylabel(r'$\mu_{eq}$ (Normalized Grayscale)')
    plt.grid(True)
    plt.tight_layout()
    plot_save_path = os.path.join(output_dir, f'mu_eq_curve_res{resolution}.png')
    plt.savefig(plot_save_path, dpi=150)
    print(f"μ_eq curve plot saved to: {plot_save_path}")
    plt.show()

def main():
    # 1. Read grayscale values from CSV
    if not os.path.exists(csv_path):
        print(f"ERROR: CSV file not found: {csv_path}")
        return
    grayscale_values = get_line_grayscale(csv_path)
    print("Grayscale values read from CSV:", grayscale_values)

    # 2. Calculate μ_eq
    mu_eq_arr = calculate_μeq(grayscale_values)
    print("μ_eq values (first 10):", mu_eq_arr[:10])

    # 3. Plot μ_eq curve
    plot_μeq_curve(mu_eq_arr)

if __name__ == '__main__':
    main()
