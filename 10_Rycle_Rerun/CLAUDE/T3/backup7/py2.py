import os
import sys

def verify_outputs():
    """
    Verify if the output files from py1.py exist
    """
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup7"
    
    # Check if directory exists
    if not os.path.exists(output_dir):
        print("Output directory does not exist.")
        return False
    
    # Check for CSV files and PNG files
    csv_files = [f for f in os.listdir(output_dir) if f.endswith('_gap_analysis.csv')]
    png_files = [f for f in os.listdir(output_dir) if f.endswith('_gap_highlight.png')]
    
    # Check if we have files for each of the 5 Poly images processed
    if len(csv_files) == 5 and len(png_files) == 5:
        print("Calculation successful")
        return True
    else:
        print(f"Expected 5 CSV and 5 PNG files, but found {len(csv_files)} CSV files and {len(png_files)} PNG files.")
        return False

if __name__ == "__main__":
    verify_outputs()
