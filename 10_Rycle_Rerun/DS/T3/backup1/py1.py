import os
import csv
import cv2
from PIL import Image
import numpy as np

def enhance_spot_image(img):
    """Apply CLAHE enhancement to the input image (supports both grayscale and color)."""
    if len(img.shape) == 3 and img.shape[2] == 3:  # Color image
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(10, 10))
        l_clahe = clahe.apply(l)
        enhanced_lab = cv2.merge([l_clahe, a, b])
        enhanced_img = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        return enhanced_img
    else:  # Grayscale image
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(10, 10))
        enhanced_img = clahe.apply(img)
        return enhanced_img

def check_gap_conditions(gray_array):
    """Determine GAP flags based on grayscale value and adjacent pixel continuity."""
    cond1 = (gray_array >= 1) & (gray_array <= 150)
    gap_flag = np.zeros_like(gray_array, dtype=np.uint8)
    height, width = gray_array.shape
    rows, cols = np.where(cond1)
    
    for r, c in zip(rows, cols):
        directions = [
            (0, -1, 25, lambda r, c, i: (r, c - i)),  # Left
            (0, 1, 25, lambda r, c, i: (r, c + i)),   # Right
            (-1, 0, 25, lambda r, c, i: (r - i, c)),  # Up
            (1, 0, 25, lambda r, c, i: (r + i, c))    # Down
        ]
        
        for dr, dc, req_length, coord_func in directions:
            count = 0
            for i in range(1, req_length + 1):
                nr, nc = coord_func(r, c, i)
                if 0 <= nr < height and 0 <= nc < width:
                    if cond1[nr, nc]:
                        count += 1
                    else:
                        break
                else:
                    break
            if count >= req_length:
                gap_flag[r, c] = 1
                break
    return gap_flag

def save_csv(gray_array, gap_flag, output_dir, base_filename):
    """Save pixel analysis data to a CSV file."""
    csv_filename = os.path.splitext(base_filename)[0] + '_gap_analysis.csv'
    csv_path = os.path.join(output_dir, csv_filename)
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['row', 'column', 'grayscale_value', 'GAP_flag'])
        height, width = gray_array.shape
        for r in range(height):
            for c in range(width):
                writer.writerow([r, c, gray_array[r, c], gap_flag[r, c]])

def process_new_images(gap_flag, output_dir, base_filename):
    """Generate and save a PNG highlighting GAP pixels in black (non-GAP in white)."""
    height, width = gap_flag.shape
    img = np.full((height, width, 3), 255, dtype=np.uint8)  # White background
    img[gap_flag == 1] = [0, 0, 0]  # Set GAP pixels to black
    img_pil = Image.fromarray(img)
    output_path = os.path.join(output_dir, os.path.splitext(base_filename)[0] + '_gap.png')
    img_pil.save(output_path)

def process_images(input_directory):
    """Process all Poly_*.png/jpg images: enhance, analyze, and save outputs."""
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T3\backup1"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_directory):
        if filename.lower().startswith("poly_") and (filename.lower().endswith('.png') or filename.lower().endswith('.jpg')):
            path = os.path.join(input_directory, filename)
            img = cv2.imread(path)
            if img is None:
                print(f"Failed to read {path}")
                continue
            
            # Enhance image and save
            enhanced_img = enhance_spot_image(img)
            enhanced_path = os.path.join(output_dir, filename)
            cv2.imwrite(enhanced_path, enhanced_img)
            
            # Convert to grayscale using PIL
            with Image.open(enhanced_path) as img_pil:
                gray_img = img_pil.convert('L')
                gray_array = np.array(gray_img)
            
            # Analyze GAP conditions
            gap_flag = check_gap_conditions(gray_array)
            
            # Save outputs
            save_csv(gray_array, gap_flag, output_dir, filename)
            process_new_images(gap_flag, output_dir, filename)

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    process_images(input_directory)
    print("Processed all images!")
