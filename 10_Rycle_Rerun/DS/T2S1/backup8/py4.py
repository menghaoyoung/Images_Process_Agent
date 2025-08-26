import os
import sys
import math
from PIL import Image

def bresenham(start, end):
    x0, y0 = start
    x1, y1 = end
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

def get_line_grayscale(image, start, end):
    points = bresenham(start, end)
    grayscale_vals = []
    for (x, y) in points:
        if 0 <= x < image.width and 0 <= y < image.height:
            grayscale_vals.append(image.getpixel((x, y)))
        else:
            grayscale_vals.append(0)
    return grayscale_vals

def main():
    # Parse command line arguments
    resolution = None
    for arg in sys.argv[1:]:
        if arg.startswith('-resolution='):
            try:
                resolution = float(arg.split('=')[1])
            except ValueError:
                print("Error: Resolution value must be a number.")
                sys.exit(1)
    
    if resolution is None:
        print("Error: Resolution not provided. Use -resolution=<value>")
        sys.exit(1)
        
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup8"
    start_point = (152, 29)
    end_point = (136, 91)
    
    # Create output directory if missing
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Verify image exists
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        sys.exit(1)
    
    # Process image
    try:
        image = Image.open(image_path)
        if image.mode != 'L':
            image = image.convert('L')
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)
    
    # Get grayscale values
    grayscale_vals = get_line_grayscale(image, start_point, end_point)
    
    # Calculate real length
    dx = end_point[0] - start_point[0]
    dy = end_point[1] - start_point[1]
    pixel_dist = math.sqrt(dx*dx + dy*dy)
    real_length = pixel_dist * resolution
    print(f"Segment length: {real_length:.2f} units")
    
    # Generate CSV filename
    csv_filename = f"line_gray_values_res_{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    # Save results
    try:
        with open(csv_path, 'w') as f:
            f.write("\n".join(map(str, grayscale_vals)))
        print(f"CSV saved to: {csv_path}")
        print("Calculation successful")
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
