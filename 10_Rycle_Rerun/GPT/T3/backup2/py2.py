import os
import sys
import time

def list_files(directory, prefix, suffixes):
    """List files in directory with given prefix and suffixes."""
    files = []
    for f in os.listdir(directory):
        if f.startswith(prefix) and f.lower().endswith(suffixes):
            files.append(f)
    return files

def check_outputs(image_names, outdir):
    """Check if for each image, the CSV and PNG GAP files exist in outdir."""
    all_exist = True
    for imname in image_names:
        base, _ = os.path.splitext(imname)
        csv_name = f"{base}_gap_analysis.csv"
        png_name = f"{base}_GAP_flag.png"
        csv_path = os.path.join(outdir, csv_name)
        png_path = os.path.join(outdir, png_name)
        if not (os.path.isfile(csv_path) and os.path.isfile(png_path)):
            print(f"Missing output for {imname}:")
            if not os.path.isfile(csv_path):
                print(f"  Missing CSV: {csv_path}")
            if not os.path.isfile(png_path):
                print(f"  Missing PNG: {png_path}")
            all_exist = False
    return all_exist

if __name__ == "__main__":
    # Input and output directories (should match those in py1.py)
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T3\backup2"

    # Run py1.py in the background
    print("Running py1.py ...")
    # Using sys.executable to ensure correct Python version
    exitcode = os.system(f'"{sys.executable}" py1.py')
    if exitcode != 0:
        print("py1.py did not finish successfully.")
        sys.exit(1)

    print("Checking for output files ...")
    # Sleep shortly to allow file system to flush
    time.sleep(1)

    # List input images
    input_imgs = list_files(input_directory, "Poly_", ('.png', '.jpg', '.jpeg'))

    # Check outputs
    if check_outputs(input_imgs, output_directory):
        print("Calculation successful")
    else:
        print("Calculation failed: Some output files are missing.")
