import os
import sys
import csv
import cv2
import numpy as np
from PIL import Image

def enhance_spot_image(image_path, output_directory):
    """Read an image, apply CLAHE enhancement, and save the result."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error loading image: {image_path}")
        return None, None
    
    # Handle grayscale and color images
    if len(img.shape) == 2:  # Grayscale
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(10, 10))
        img_clahe = clahe.apply(img)
    else:  # Color (convert to LAB space first)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(10, 10))
        l_clahe = clahe.apply(l)
        lab_clahe = cv2.merge([l_clahe, a, b])
        img_clahe = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
    
    # Save CLAHE-enhanced image
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    clahe_path = os.path.join(output_directory, f"{base_name}_clahe.png")
    cv2.imwrite(clahe_path, img_clahe)
    return clahe_path, base_name

def check_gap_conditions(gray_array):
    """Identify GAP pixels based on grayscale value and adjacent conditions."""
    height, width = gray_array.shape
    mask_cond1 = (gray_array >= 1) & (gray_array <= 150)
    mask_uint8 = np.uint8(mask_cond1 * 255)
    
    # Find connected components
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask_uint8, connectivity=4)
    
    # Identify regions with >=25 contiguous pixels
    large_region = np.zeros_like(mask_cond1, dtype=bool)
    for label in range(1, num_labels):
        if stats[label, cv2.CC_STAT_AREA] >= 25:
            large_region[labels == label] = True
    
    # Check adjacent pixels for large regions
    condition2 = np.zeros_like(large_region, dtype=bool)
    if height > 1 and width > 0:  # Vertical checks
        condition2[1:, :] |= large_region[:-1, :]  # Up
        condition2[:-1, :] |= large_region[1:, :]   # Down
    if height > 0 and width > 1:  # Horizontal checks
        condition2[:, 1:] |= large_region[:, :-1]   # Left
        condition2[:, :-1] |= large_region[:, 1:]   # Right
    
    return mask_cond1 & condition2

def save_csv(gray_array, gap_flags, base_name, output_directory):
    """Save pixel analysis data to a CSV file."""
    csv_path = os.path.join(output_directory, f"{base_name}_gap_analysis.csv")
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Row", "Column", "Grayscale", "GAP_Flag"])
        for i in range(gray_array.shape[0]):
            for j in range(gray_array.shape[1]):
                writer.writerow([i, j, gray_array[i, j], int(gap_flags[i, j])])

def create_gap_image(gap_flags, base_name, output_directory):
    """Generate a PNG image highlighting GAP pixels."""
    img_array = np.full((*gap_flags.shape, 3), 255, dtype=np.uint8)  # White background
    img_array[gap_flags] = [0, 0, 0]  # Black for GAP pixels
    img = Image.fromarray(img_array)
    img.save(os.path.join(output_directory, f"{base_name}_gap_flag.png"))

def process_images(input_directory, output_directory):
    """Process all images in the input directory."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    valid_exts = ('.png', '.jpg', '.jpeg')
    for filename in os.listdir(input_directory):
        if filename.lower().startswith('poly_') and filename.lower().endswith(valid_exts):
            image_path = os.path.join(input_directory, filename)
            clahe_path, base_name = enhance_spot_image(image_path, output_directory)
            if clahe_path is None:
                continue
            
            # Process with PIL
            img_pil = Image.open(clahe_path)
            gray_img = img_pil.convert('L')
            gray_array = np.array(gray_img)
            
            # Identify GAP pixels
            gap_flags = check_gap_conditions(gray_array)
            
            # Save outputs
            save_csv(gray_array, gap_flags, base_name, output_directory)
            create_gap_image(gap_flags, base_name, output_directory)

if __name__ == "__main__":
    input_dir = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T3\backup4"
    
    process_images(input_dir, output_dir)
    print("Processed all images!")
