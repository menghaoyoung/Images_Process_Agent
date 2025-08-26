# py2.py - Program to verify outputs from py1.py
import os
import subprocess
import sys

def verify_outputs():
    # Define the output directory
    output_dir = r"C:\Users\admin\Desktop\For git\All_Outputs"
    
    # Define the base filename (from the input image)
    base_filename = "Li_1.0"
    
    # Expected output files
    expected_files = [
        f"{base_filename}_grayscale_values.csv",
        f"{base_filename}_line_length.txt",
        f"{base_filename}_u_eq_values.csv",
        f"{base_filename}_u_eq_plot.tiff"
    ]
    
    # Run py1.py with resolution=1.08
    try:
        subprocess.run(["python", "py1.py", "-resolution=1.08"], check=True)
    except subprocess.CalledProcessError:
        print("Error running py1.py")
        return False
    
    # Check if all expected files exist
    all_files_exist = True
    for filename in expected_files:
        file_path = os.path.join(output_dir, filename)
        if not os.path.exists(file_path):
            print(f"Missing file: {file_path}")
            all_files_exist = False
    
    if all_files_exist:
        print("Calculation successful")
        return True
    else:
        return False

if __name__ == "__main__":
    verify_outputs()
