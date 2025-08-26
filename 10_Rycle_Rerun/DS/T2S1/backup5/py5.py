import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math
import argparse
import csv
import subprocess
import time

def bresenham_line(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    points = []
    
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return points

def process_image(resolution, image_path, output_dir, start_point, end_point):
    """Process single image with given resolution"""
    print(f"\nProcessing resolution: {resolution}")
    
    # Open and convert image
    img = Image.open(image_path)
    if img.mode != 'L':
        img = img.convert('L')
    img_array = np.array(img)
    
    # Generate line coordinates
    x0, y0 = start_point
    x1, y1 = end_point
    line_coords = bresenham_line(x0, y0, x1, y1)
    
    # Extract grayscale values
    grayscale_values = []
    for x, y in line_coords:
        if 0 <= y < img_array.shape[0] and 0 <= x < img_array.shape[1]:
            grayscale_values.append(img_array[y, x])
        else:
            grayscale_values.append(0)
    
    # Calculate real length
    pixel_distance = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
    real_length = pixel_distance * resolution
    
    # Save to CSV
    safe_res = str(resolution).replace('.', '_')
    csv_filename = f"grayscale_values_res_{safe_res}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    np.savetxt(csv_path, grayscale_values, fmt='%d', delimiter=',')
    print(f"- CSV saved: {csv_path}")
    
    # Create visualization
    plt.figure(figsize=(10, 5))
    plt.plot(grayscale_values, 'b-', linewidth=1.5)
    plt.title(f"Grayscale Profile (Res: {resolution}, Length: {real_length:.2f} units)")
    plt.xlabel("Pixel Position")
    plt.ylabel("Grayscale Value")
    plt.grid(alpha=0.3)
    
    plot_filename = f"profile_res_{safe_res}.png"
    plot_path = os.path.join(output_dir, plot_filename)
    plt.savefig(plot_path, dpi=120)
    plt.close()
    print(f"- Visualization saved: {plot_path}")
    
    return real_length, grayscale_values

def generate_report(resolutions, lengths, output_dir):
    """Generate comprehensive analysis report"""
    report_path = os.path.join(output_dir, "analysis_report.txt")
    with open(report_path, 'w') as f:
        f.write("Image Line Segment Analysis Report\n")
        f.write("="*50 + "\n\n")
        
        f.write("Processing Parameters:\n")
        f.write(f"- Start Point: (152, 29)\n")
        f.write(f"- End Point: (136, 91)\n")
        f.write(f"- Image: Li_1.0.png\n\n")
        
        f.write("Resolution Analysis:\n")
        f.write("Resolution (units/pixel) | Real Length (units)\n")
        f.write("-"*45 + "\n")
        for res, length in zip(resolutions, lengths):
            f.write(f"{res:>20.4f} | {length:>18.2f}\n")
        
        f.write("\nConclusion:\n")
        f.write(f"Processed {len(resolutions)} resolution values. ")
        f.write("All outputs saved in the output directory.")
    
    print(f"\nReport generated: {report_path}")

def main():
    # Configuration
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup5"
    start_point = (152, 29)
    end_point = (136, 91)
    resolutions = [0.5, 1.0, 1.08, 1.5, 2.0]  # Multiple resolutions to process
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all resolutions
    lengths = []
    for res in resolutions:
        real_length, _ = process_image(res, image_path, output_dir, start_point, end_point)
        lengths.append(real_length)
    
    # Verify outputs
    print("\nVerifying outputs:")
    for res in resolutions:
        safe_res = str(res).replace('.', '_')
        csv_path = os.path.join(output_dir, f"grayscale_values_res_{safe_res}.csv")
        if os.path.exists(csv_path):
            print(f"- Resolution {res:.2f}: Calculation successful")
        else:
            print(f"- Resolution {res:.2f}: CSV not found")
    
    # Generate final report
    generate_report(resolutions, lengths, output_dir)
    print("\nProcessing completed successfully")

if __name__ == "__main__":
    main()
