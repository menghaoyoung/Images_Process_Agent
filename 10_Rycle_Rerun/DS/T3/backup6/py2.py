import os
import subprocess
import sys

# Define input and output directories
INPUT_DIR = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
OUTPUT_DIR = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T3\backup6"

def verify_output_files():
    """Check if output CSV and PNG files exist for all processed images."""
    all_files_exist = True
    for filename in os.listdir(INPUT_DIR):
        if filename.startswith("Poly_") and filename.lower().endswith(('.png', '.jpg')):
            base_name = os.path.splitext(filename)[0]
            csv_file = f"{base_name}_gap_analysis.csv"
            png_file = f"{base_name}_gap_highlight.png"
            
            csv_path = os.path.join(OUTPUT_DIR, csv_file)
            png_path = os.path.join(OUTPUT_DIR, png_file)
            
            if not (os.path.exists(csv_path) and os.path.exists(png_path)):
                print(f"Missing output files for: {base_name}")
                print(f"Expected CSV: {csv_path}")
                print(f"Expected PNG: {png_path}")
                all_files_exist = False
    
    return all_files_exist

def main():
    # Run py1.py as a background process
    try:
        process = subprocess.Popen(
            [sys.executable, "py1.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Running py1.py in background...")
        stdout, stderr = process.communicate()  # Wait for process to complete
        
        if process.returncode != 0:
            print(f"Error running py1.py (exit code: {process.returncode})")
            print("Error output:")
            print(stderr)
            return
        
    except Exception as e:
        print(f"Failed to execute py1.py: {str(e)}")
        return
    
    # Verify output files
    if verify_output_files():
        print("Calculation successful")
    else:
        print("Verification failed: Some output files are missing")

if __name__ == "__main__":
    main()
