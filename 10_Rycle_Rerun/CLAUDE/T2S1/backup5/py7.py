# py2.py - Program to verify if CSV files exist after running py1.py
import os
import subprocess
import time

# Define the output directory path
output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup5"

def check_csv_exists(resolution):
    """Check if the CSV file for a specific resolution exists"""
    csv_filename = f"grayscale_values_res{resolution}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    return os.path.exists(csv_path)

def main():
    # Set the resolution
    resolution = 1.08
    
    # Check if py1.py exists in the current directory
    if not os.path.exists("py1.py"):
        print("Error: py1.py not found in the current directory")
        return
    
    # Run py1.py with the specified resolution
    print(f"Running py1.py with resolution={resolution}...")
    
    # Start the process
    process = subprocess.Popen(["python", "py1.py", f"-resolution={resolution}"], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for a short time to allow the process to start
    print("Waiting for processing to complete...")
    time.sleep(2)
    
    # Check if the process is still running
    if process.poll() is None:
        print("py1.py is still running in the background")
    
    # Wait for a reasonable time for the file to be created
    max_wait = 30  # seconds
    wait_interval = 2  # seconds
    total_wait = 0
    
    while total_wait < max_wait:
        if check_csv_exists(resolution):
            print("Calculation successful")
            return
        time.sleep(wait_interval)
        total_wait += wait_interval
        print(f"Waiting... ({total_wait}/{max_wait} seconds)")
    
    # If we get here, the file wasn't found within the time limit
    print(f"Calculation failed: CSV file not found after {max_wait} seconds")
    
    # Check if the process is still running and kill it if necessary
    if process.poll() is None:
        print("Terminating py1.py process...")
        process.terminate()

if __name__ == "__main__":
    main()
