import os
import numpy as np
import matplotlib.pyplot as plt
import csv

def main():
    # Define parameters
    resolution = 1.08
    csv_filename = f"grayscale_values_res_{str(resolution).replace('.', '_')}.csv"
    input_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup5"
    csv_path = os.path.join(input_dir, csv_filename)
    
    # Read values from CSV
    grayscale_values = []
    with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            grayscale_values.append(int(row[0]))
    
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot(grayscale_values, 'b-', linewidth=2)
    plt.title(f"Grayscale Profile Along Line Segment (Resolution: {resolution})")
    plt.xlabel("Pixel Position Along Line")
    plt.ylabel("Grayscale Value (0-255)")
    plt.grid(True, alpha=0.3)
    
    # Highlight min/max values
    min_val, max_val = min(grayscale_values), max(grayscale_values)
    min_idx = grayscale_values.index(min_val)
    max_idx = grayscale_values.index(max_val)
    plt.scatter(min_idx, min_val, color='red', zorder=5, label=f'Min: {min_val}')
    plt.scatter(max_idx, max_val, color='green', zorder=5, label=f'Max: {max_val}')
    
    plt.legend()
    plt.tight_layout()
    
    # Save and show plot
    output_path = os.path.join(input_dir, f"grayscale_profile_res_{str(resolution).replace('.', '_')}.png")
    plt.savefig(output_path, dpi=150)
    print(f"Plot saved to: {output_path}")
    plt.show()

if __name__ == "__main__":
    main()
