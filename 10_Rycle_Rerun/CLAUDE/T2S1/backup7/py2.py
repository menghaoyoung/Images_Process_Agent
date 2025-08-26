import os
import subprocess
import time
import sys

def run_and_verify():
    # Define paths
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup7"
    expected_csv = os.path.join(output_dir, "line_grayscale_res_1.08.csv")
    expected_npy = os.path.join(output_dir, "line_grayscale_res_1.08.npy")
    expected_plot = os.path.join(output_dir, "line_grayscale_plot_res_1.08.png")
    
    # Run py1.py with resolution=1.08
    print("Running py1.py with resolution=1.08...")
    try:
        # Run the program in a subprocess
        process = subprocess.Popen(
            ["python", "py1.py", "-resolution=1.08"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Get output and errors
        stdout, stderr = process.communicate()
        
        # Print output for debugging
        print("Output from py1.py:")
        print(stdout)
        
        if stderr:
            print("Errors from py1.py:")
            print(stderr)
            
        # Wait a moment to ensure file operations complete
        time.sleep(2)
        
        # Check if the files exist
        csv_exists = os.path.exists(expected_csv)
        npy_exists = os.path.exists(expected_npy)
        plot_exists = os.path.exists(expected_plot)
        
        if csv_exists and npy_exists and plot_exists:
            print("\nCalculation successful")
            print(f"CSV file exists: {expected_csv}")
            print(f"NumPy file exists: {expected_npy}")
            print(f"Plot file exists: {expected_plot}")
            
            # Display file sizes for verification
            csv_size = os.path.getsize(expected_csv)
            npy_size = os.path.getsize(expected_npy)
            print(f"CSV file size: {csv_size} bytes")
            print(f"NumPy file size: {npy_size} bytes")
            
            return True
        else:
            print("\nCalculation failed or files not found:")
            print(f"CSV file exists: {csv_exists}")
            print(f"NumPy file exists: {npy_exists}")
            print(f"Plot file exists: {plot_exists}")
            return False
            
    except Exception as e:
        print(f"Error running py1.py: {e}")
        return False

if __name__ == "__main__":
    run_and_verify()
