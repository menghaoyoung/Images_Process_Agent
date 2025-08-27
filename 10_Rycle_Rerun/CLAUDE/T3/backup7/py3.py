import os
import sys
import subprocess

def ensure_directory_exists(directory):
    """
    Ensure the specified directory exists, create it if it doesn't
    """
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def run_py1():
    """
    Run py1.py and capture its output
    """
    print("Running py1.py...")
    try:
        result = subprocess.run(["python", "py1.py"], capture_output=True, text=True)
        print("py1.py output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
    except Exception as e:
        print(f"Error running py1.py: {e}")

def verify_outputs():
    """
    Verify if the output files from py1.py exist
    """
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup7"
    
    # Ensure the output directory exists
    ensure_directory_exists(output_dir)
    
    # Check if directory exists
    if not os.path.exists(output_dir):
        print(f"Output directory does not exist: {output_dir}")
        return False
    
    # Check for CSV files and PNG files
    files = os.listdir(output_dir)
    csv_files = [f for f in files if f.endswith('_gap_analysis.csv')]
    png_files = [f for f in files if f.endswith('_gap_highlight.png')]
    
    print(f"Found {len(csv_files)} CSV files and {len(png_files)} PNG files in {output_dir}")
    
    if len(csv_files) > 0 and len(png_files) > 0:
        print("Calculation successful")
        return True
    else:
        print("Missing output files. Checking enhanced directory...")
        
        # Check if there's an "enhanced" subdirectory
        enhanced_dir = os.path.join(output_dir, "enhanced")
        if os.path.exists(enhanced_dir):
            enhanced_files = os.listdir(enhanced_dir)
            print(f"Found {len(enhanced_files)} files in enhanced directory")
            
            # If there are enhanced images but no output files, there might be an issue with the processing
            if len(enhanced_files) > 0:
                print("Enhanced images exist but final outputs are missing. There might be an issue with the processing step.")
        
        return False

if __name__ == "__main__":
    # Run py1.py first
    run_py1()
    
    # Then verify outputs
    verify_outputs()
