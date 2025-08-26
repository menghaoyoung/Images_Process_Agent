import os
import subprocess
import sys
import time
import argparse

def main():
    # Set fixed parameters from task description
    resolution = 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup9"
    csv_filename = f"grayscale_values_res_{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    print(f"Running py1.py with resolution {resolution}...")
    
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Clean up existing CSV file if present
        if os.path.exists(csv_path):
            os.remove(csv_path)
            print(f"Removed existing file: {csv_path}")
        
        # Run py1.py with required resolution argument
        command = [sys.executable, "py1.py", f"-resolution={resolution}"]
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        
        # Wait for process to complete
        stdout, stderr = process.communicate(timeout=30)
        
        # Check process results
        if process.returncode != 0:
            print(f"py1.py failed with exit code: {process.returncode}")
            if stderr:
                print("Error details:")
                print(stderr.decode().strip())
            sys.exit(1)
        
        # Verify CSV file creation
        if os.path.exists(csv_path):
            print("\nCalculation successful")
            print(f"CSV file created at: {csv_path}")
            print(f"File size: {os.path.getsize(csv_path)} bytes")
        else:
            print("\nError: CSV file not created")
            print("Expected file path:", csv_path)
            print("Directory contents:")
            for f in os.listdir(output_dir):
                print(f" - {f}")
            sys.exit(1)
    
    except subprocess.TimeoutExpired:
        print("Error: py1.py execution timed out after 30 seconds")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
