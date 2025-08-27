import os
import csv
import cv2
import numpy as np
from PIL import Image

def enhance_spot_image(img):
    """Apply CLAHE enhancement to an image."""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(10, 10))
    l_clahe = clahe.apply(l)
    lab_clahe = cv2.merge((l_clahe, a, b))
    enhanced_bgr = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
    return enhanced_bgr

def compute_run_lengths(valid):
    """Compute horizontal and vertical run lengths for valid pixels."""
    rows, cols = valid.shape
    # Horizontal runs
    left_pass = np.zeros_like(valid, dtype=int)
    for i in range(rows):
        for j in range(cols):
            if valid[i, j]:
                left_pass[i, j] = left_pass[i, j-1] + 1 if j > 0 else 1
    
    right_pass = np.zeros_like(valid, dtype=int)
    for i in range(rows):
        for j in range(cols-1, -1, -1):
            if valid[i, j]:
                right_pass[i, j] = right_pass[i, j+1] + 1 if j < cols-1 else 1
    
    horiz_run = left_pass + right_pass - 1
    
    # Vertical runs
    top_pass = np.zeros_like(valid, dtype=int)
    for j in range(cols):
        for i in range(rows):
            if valid[i, j]:
                top_pass[i, j] = top_pass[i-1, j] + 1 if i > 0 else 1
    
    bottom_pass = np.zeros_like(valid, dtype=int)
    for j in range(cols):
        for i in range(rows-1, -1, -1):
            if valid[i, j]:
                bottom_pass[i, j] = bottom_pass[i+1, j] + 1 if i < rows-1 else 1
    
    vert_run = top_pass + bottom_pass - 1
    return horiz_run, vert_run

def check_gap_conditions(gray_array):
    """Identify GAP pixels based on grayscale conditions."""
    valid = (gray_array >= 1) & (gray_array <= 150)
    horiz_run, vert_run = compute_run_lengths(valid)
    has_long_run = (horiz_run >= 25) | (vert_run >= 25)
    
    # Propagate long-run flags to neighbors
    condition2 = np.zeros_like(valid, dtype=bool)
    condition2[1:, :] |= has_long_run[:-1, :]   # Top neighbor
    condition2[:-1, :] |= has_long_run[1:, :]   # Bottom neighbor
    condition2[:, 1:] |= has_long_run[:, :-1]   # Left neighbor
    condition2[:, :-1] |= has_long_run[:, 1:]   # Right neighbor
    gap_flag = valid & condition2
    return gap_flag

def save_csv(output_path, gray_array, gap_flag):
    """Save pixel data to a CSV file."""
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['row', 'column', 'gray_value', 'gap_flag'])
        rows, cols = gray_array.shape
        for i in range(rows):
            for j in range(cols):
                writer.writerow([i, j, gray_array[i, j], int(gap_flag[i, j])])

def process_new_image(output_path, gap_flag):
    """Generate binary output image highlighting GAP pixels."""
    result_img = np.full((*gap_flag.shape, 3), 255, dtype=np.uint8)  # White background
    result_img[gap_flag] = [0, 0, 0]  # Black for GAP pixels
    Image.fromarray(result_img, 'RGB').save(output_path)

def process_images(input_directory, output_directory):
    """Process all images in the input directory."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for filename in os.listdir(input_directory):
        if filename.startswith("Poly_") and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_directory, filename)
            img = cv2.imread(img_path)
            if img is None:
                continue
            
            base_name = os.path.splitext(filename)[0]
            # Process CLAHE enhancement
            enhanced_bgr = enhance_spot_image(img)
            # Save enhanced image
            enhanced_path = os.path.join(output_directory, f"{base_name}_enhanced.png")
            cv2.imwrite(enhanced_path, enhanced_bgr)
            
            # Convert to grayscale with PIL
            enhanced_rgb = cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2RGB)
            gray_img = Image.fromarray(enhanced_rgb).convert('L')
            gray_array = np.array(gray_img)
            
            # Identify GAP pixels
            gap_flag = check_gap_conditions(gray_array)
            
            # Save CSV analysis
            csv_path = os.path.join(output_directory, f"{base_name}_gap_analysis.csv")
            save_csv(csv_path, gray_array, gap_flag)
            
            # Generate output image
            img_output_path = os.path.join(output_directory, f"{base_name}_gap_map.png")
            process_new_image(img_output_path, gap_flag)

if __name__ == "__main__":
    input_dir = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T3\backup3"
    process_images(input_dir, output_dir)
    print("Processed all images!")
