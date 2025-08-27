import os
import glob

def verify_outputs():
    """Verify if the output files from py1.py exist"""
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup8"
    
    # Check if output files exist
    png_files = glob.glob(os.path.join(output_dir, "*_gap_result.png"))
    csv_files = glob.glob(os.path.join(output_dir, "*_gap_analysis.csv"))
    
    print(f"Checking for output files in: {output_dir}")
    
    if png_files and csv_files:
        print("Calculation successful")
        print(f"Found {len(png_files)} PNG files and {len(csv_files)} CSV files")
        for png in png_files:
            print(f"  - {os.path.basename(png)}")
        return True
    else:
        print("Calculation failed")
        print(f"Found {len(png_files)} PNG files and {len(csv_files)} CSV files")
        return False

if __name__ == "__main__":
    verify_outputs()
