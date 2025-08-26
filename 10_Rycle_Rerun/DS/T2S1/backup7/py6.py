import os
import numpy as np
import argparse
from PIL import Image
import math
import sys

def bresenham(x0, y0, x1, y1):
    """Bresenham's line algorithm for integer coordinate generation"""
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
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

def main():
    # Robust argument handling that accepts any format
    resolution_value = None
    
    # Check if arguments were passed at all
    if len(sys.argv) > 1:
        # Handle both -resolution=1.08 and -resolution 1.08 formats
        for i, arg in enumerate(sys.argv[1:]):
            if arg.startswith('-resolution'):
                if '=' in arg:
                    # Format: -resolution=1.08
                    resolution_value = float(arg.split('=')[1])
                else:
                    # Format: -resolution 1.08
                    if i+2 < len(sys.argv):
                        resolution_value = float(sys.argv[i+2])
    
    # If still not found, show error and exit
    if resolution_value is None:
        print("ERROR: Missing required -resolution argument")
        print("Usage: python program.py -resolution=1.08")
        print("   OR: python program.py -resolution 1.08")
        sys.exit(1)
        
    resolution = resolution_value
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    start_point = (152, 29)
    end_point = (136, 91)
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup7"
    
    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)
    
    # Handle image loading errors
    try:
        image = Image.open(image_path).convert('L')
    except FileNotFoundError:
        print(f"ERROR: Image not found at {image_path}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR loading image: {str(e)}")
        sys.exit(1)
    
    # Calculate physical length
    dx = start_point[0] - end_point[0]
    dy = start_point[1] - end_point[1]
    distance_pixels = math.sqrt(dx**2 + dy**2)
    physical_length = distance_pixels * resolution
    print(f"Physical segment length: {physical_length:.2f} units")
    
    # Get all points along the line
    line_points = bresenham(start_point[0], start_point[1], 
                            end_point[0], end_point[1])
    
    # Extract grayscale values with bounds checking
    grayscale_values = []
    for x, y in line_points:
        try:
            # Verify point is within image bounds
            if 0 <= x < image.width and 0 <= y < image.height:
                grayscale_values.append(image.getpixel((x, y)))
            else:
                print(f"Warning: Point ({x}, {y}) out of bounds. Using 0.")
                grayscale_values.append(0)
        except Exception as e:
            print(f"Error accessing pixel ({x}, {y}): {str(e)}")
            grayscale_values.append(0)
    
    # Save to CSV file
    csv_filename = f"grayscale_values_res_{resolution}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    np.savetxt(csv_path, grayscale_values, fmt='%d', delimiter=',')
    print(f"Saved {len(grayscale_values)} values to {csv_path}")

if __name__ == '__main__':
    main()
