import os
import csv
import cv2
from PIL import Image
import numpy as np

def enhance_spot_image(input_image_path, output_image_path):
    """
    Apply CLAHE enhancement to the input image and save to output path.
    """
    img = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
    if img is None:
        print(f"Failed to read image: {input_image_path}")
        return False
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(10, 10))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    cv2.imwrite(output_image_path, enhanced_img)
    print(f"CLAHE enhanced image saved to: {output_image_path}")
    return True

def check_gap_conditions(gray_array, row, col):
    """
    For pixel at (row, col), check:
    (1) Grayscale value between 1–150 (inclusive)
    (2) At least one direction (up, down, left, right) has 25 contiguous pixels meeting the grayscale condition.
    Return True if GAP, False otherwise.
    """
    h, w = gray_array.shape
    pixel_val = gray_array[row, col]
    if not (1 <= pixel_val <= 150):
        return False

    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        contiguous = 0
        for k in range(1, 26):  # 1 to 25
            r, c = row + dr * k, col + dc * k
            if 0 <= r < h and 0 <= c < w:
                neighbor_val = gray_array[r, c]
                if 1 <= neighbor_val <= 150:
                    contiguous += 1
                else:
                    break
            else:
                break
        if contiguous == 25:
            return True
    return False

def process_new_images(gray_array, gap_flag_array, output_png_path):
    """
    Generate a new PNG image with GAP flag pixels in black, others in white.
    """
    h, w = gray_array.shape
    new_img = np.full((h, w, 3), 255, dtype=np.uint8)  # default white
    new_img[gap_flag_array == 1] = [0, 0, 0]  # GAP in black
    Image.fromarray(new_img).save(output_png_path)
    print(f"GAP-highlighted image saved to: {output_png_path}")

def save_csv(row_col_gray_gap_list, output_csv_path):
    """
    Save all pixel data to CSV: row, column, grayscale, GAP flag
    """
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['row', 'col', 'gray', 'GAP'])
        writer.writerows(row_col_gray_gap_list)
    print(f"CSV file saved to: {output_csv_path}")

def process_images(input_directory):
    """
    Main processing function: finds Poly_*.png/jpg, enhances, analyzes, saves results.
    """
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T3\backup"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Search for Poly_*.png/jpg (case-insensitive)
    image_files = [f for f in os.listdir(input_directory)
                   if f.lower().startswith("poly_") and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print("No input images found.")
        return

    for fname in image_files:
        in_path = os.path.join(input_directory, fname)
        base, ext = os.path.splitext(fname)
        clahe_fname = base + "_clahe.png"
        clahe_path = os.path.join(output_directory, clahe_fname)

        # CLAHE enhancement
        success = enhance_spot_image(in_path, clahe_path)
        if not success:
            continue

        # Open enhanced image as grayscale with PIL
        with Image.open(clahe_path) as img:
            gray_img = img.convert("L")
            gray_array = np.array(gray_img)

        h, w = gray_array.shape
        gap_flag_array = np.zeros((h, w), dtype=np.uint8)
        pixel_data = []

        # For each pixel, check GAP condition
        for row in range(h):
            for col in range(w):
                gap_flag = 1 if check_gap_conditions(gray_array, row, col) else 0
                gap_flag_array[row, col] = gap_flag
                pixel_data.append([row, col, int(gray_array[row, col]), gap_flag])
            if row % 100 == 0:
                print(f"Processing {fname}: row {row}/{h}")

        # Save CSV
        csv_fname = base + "_gap_analysis.csv"
        csv_path = os.path.join(output_directory, csv_fname)
        save_csv(pixel_data, csv_path)

        # Save new PNG
        out_png_fname = base + "_gap.png"
        out_png_path = os.path.join(output_directory, out_png_fname)
        process_new_images(gray_array, gap_flag_array, out_png_path)

        print(f"Finished processing image: {fname}")

if __name__ == "__main__":
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    process_images(input_directory)
    print("Proceed all the images！")
