import os
import subprocess
import sys

def verify_outputs():
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup"
    
    # Check if directory exists
    if not os.path.exists(output_directory):
        print("Output directory does not exist!")
        return False
    
    # Check if there are any CSV files and PNG files in the directory
    csv_files = [f for f in os.listdir(output_directory) if f.endswith('_gap_analysis.csv')]
    png_files = [f for f in os.listdir(output_directory) if f.endswith('_enhanced.png') or f.endswith('_gap_visualization.png')]
    
    if len(csv_files) > 0 and len(png_files) > 0:
        print("Calculation successful")
        return True
    else:
        print("No output files found!")
        return False

if __name__ == "__main__":
    # Run py1.py
    try:
        subprocess.run([sys.executable, "py1.py"], check=True)
        # Verify outputs
        verify_outputs()
    except subprocess.CalledProcessError:
        print("Error running py1.py")
