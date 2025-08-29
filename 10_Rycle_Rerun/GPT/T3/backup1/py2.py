import os

def check_gpt_outputs(output_dir, expected_prefix='Poly_', img_suffix='_GAP_visual.png', csv_suffix='_gap_analysis.csv'):
    """
    Checks if for each expected image, both the new image and the CSV file exist.
    Prints 'Calculation successful' if all outputs are found, else lists missing files.
    """
    # List all outputs in the backup directory
    files = os.listdir(output_dir)
    # Identify all original image base names by scanning for CLAHE images
    clahe_imgs = [f for f in files if f.startswith(expected_prefix) and f.endswith('_CLAHE.png')]
    base_names = [f.replace('_CLAHE.png','') for f in clahe_imgs]
    missing = []
    for base in base_names:
        img_file = base + img_suffix
        csv_file = base + csv_suffix
        if img_file not in files:
            missing.append(img_file)
        if csv_file not in files:
            missing.append(csv_file)
    if not missing:
        print("Calculation successful")
    else:
        print("Missing output files:")
        for f in missing:
            print(" -", f)

if __name__ == "__main__":
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T3\backup1"
    check_gpt_outputs(output_directory)
