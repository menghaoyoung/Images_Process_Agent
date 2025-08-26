import os
import subprocess
import time
import sys

def main():
    # Define parameters
    resolution = "1.08"
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup8"
    csv_filename = f"line_gray_values_res_{resolution}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    # Remove existing CSV file if present
    if os.path.exists(csv_path):
        try:
            os.remove(csv_path)
            print(f"Removed existing CSV file: {csv_path}")
        except Exception as e:
            print(f"Warning: Could not remove existing CSV - {e}")
    
    # Run py1.py as a subprocess
    try:
        print(f"Running py1.py with resolution={resolution}...")
        cmd = ["python", "py1.py", f"-resolution={resolution}"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for process completion with timeout
        try:
            stdout, stderr = process.communicate(timeout=10)
            print(stdout.decode('utf-8'))
            if stderr:
                print("Errors encountered:")
                print(stderr.decode('utf-8'))
        except subprocess.TimeoutExpired:
            process.kill()
            print("Error: py1.py execution timed out (10 seconds)")
            stdout, stderr = process.communicate()
        
        # Check exit status
        if process.returncode != 0:
            print(f"py1.py failed with exit code: {process.returncode}")
            print("Calculation failed")
            return
    
    except Exception as e:
        print(f"Error running py1.py: {str(e)}")
        print("Calculation failed")
        return
    
    # Verify CSV creation with retries
    max_retries = 5
    for i in range(max_retries):
        if os.path.exists(csv_path):
            print(f"Found CSV file: {csv_path}")
            print("Calculation successful")
            return
        print(f"Waiting for CSV creation... (attempt {i+1}/{max_retries})")
        time.sleep(1)
    
    print("Calculation failed: CSV file not created")
    print("Please check py1.py for errors or increase verification timeout")

if __name__ == "__main__":
    main()
