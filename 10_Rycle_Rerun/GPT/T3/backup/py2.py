import os

def check_output_files(output_directory):
    """
    Checks if there are any output files matching required patterns in the output directory.
    Returns True if both PNG and CSV files for at least one Poly_ image are found.
    """
    if not os.path.exists(output_directory):
        print(f"Output directory does not exist: {output_directory}")
        return False

    files = os.listdir(output_directory)
    csv_exist = any(f.startswith("Poly_") and f.endswith("_gap_analysis.csv") for f in files)
    png_exist = any(f.startswith("Poly_") and f.endswith("_gap.png") for f in files)
    if csv_exist and png_exist:
        return True
    return False

if __name__ == "__main__":
    import subprocess
    import sys
    import time

    # Path to py1.py (assumed to be in the same directory)
    py1_path = os.path.join(os.path.dirname(__file__), "py1.py")
    # Output directory as specified
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T3\backup"

    # Run py1.py in the background and wait for it to finish
    # (If it's a long process, you may want to add a timeout)
    proc = subprocess.Popen([sys.executable, py1_path])

    # Wait for process to finish
    proc.wait()

    # After running, check if output files exist
    if check_output_files(output_directory):
        print("Calculation successful")
    else:
        print("Calculation failed: output files not found.")
