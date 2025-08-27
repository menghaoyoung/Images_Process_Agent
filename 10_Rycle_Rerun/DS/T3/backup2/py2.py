# py2.py - Runs py1.py and verifies output
import os
import subprocess
import sys

def verify_output(output_dir):
    """Check if output files exist for all processed images"""
    files = os.listdir(output_dir)
    csv_count = sum(1 for f in files if f.endswith('_gap_analysis.csv'))
    png_count = sum(1 for f in files if f.endswith('_gap_highlight.png'))
    
    if csv_count > 0 and png_count > 0 and csv_count == png_count:
        print("Calculation successful")
        return True
    else:
        print(f"Verification failed: Found {csv_count} CSVs and {png_count} PNGs")
        return False

if __name__ == "__main__":
    input_dir = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T3\backup9"
    
    # Run py1.py as a background process
    process = subprocess.Popen(
        [sys.executable, "py1.py", input_dir],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for process to complete with 5 minute timeout
    try:
        stdout, stderr = process.communicate(timeout=300)
        if process.returncode != 0:
            print(f"Error running py1.py:\n{stderr.decode()}")
        else:
            verify_output(output_dir)
    except subprocess.TimeoutExpired:
        process.kill()
        print("py1.py execution timed out after 5 minutes")

# NO-RUN-PY (This program requires py1.py to be executed first)
