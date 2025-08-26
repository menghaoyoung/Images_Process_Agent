# py2.py - Program to run py1.py and verify if CSV files exist
import os
import subprocess
import sys
import time

def main():
    # Set resolution
    resolution = 1.08
    
    # Define output directory and expected CSV file
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup3"
    csv_filename = os.path.join(output_dir, f"grayscale_values_res_{resolution}.csv")
    
    # Check if CSV file already exists and delete it to ensure fresh run
    if os.path.exists(csv_filename):
        try:
            os.remove(csv_filename)
            print(f"Removed existing CSV file: {csv_filename}")
        except Exception as e:
            print(f"Warning: Could not remove existing CSV file: {e}")
    
    # Run py1.py in the background with the resolution parameter
    print(f"Running py1.py with resolution={resolution} in the background...")
    
    try:
        # Use subprocess.Popen to run py1.py in the background
        process = subprocess.Popen(
            [sys.executable, "py1.py", "-resolution", str(resolution)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print(f"Started py1.py (PID: {process.pid})")
        
        # Wait a bit to give the process time to create the file
        print("Waiting for the process to complete...")
        time.sleep(5)  # Wait 5 seconds
        
        # Check if the process is still running
        if process.poll() is None:
            print("Process is still running...")
        else:
            stdout, stderr = process.communicate()
            exit_code = process.returncode
            if exit_code != 0:
                print(f"Warning: py1.py exited with code {exit_code}")
                print(f"stderr: {stderr.decode('utf-8', errors='replace')}")
    
    except Exception as e:
        print(f"Error running py1.py: {e}")
        return
    
    # Check if the CSV file exists
    print("\nChecking if CSV file exists...")
    if os.path.exists(csv_filename):
        print(f"CSV file found at: {csv_filename}")
        print("Calculation successful")
    else:
        print(f"CSV file not found at: {csv_filename}")
        print("Waiting a bit longer...")
        
        # Wait a bit longer and check again
        time.sleep(10)  # Wait 10 more seconds
        
        if os.path.exists(csv_filename):
            print(f"CSV file found after waiting at: {csv_filename}")
            print("Calculation successful")
        else:
            print(f"CSV file still not found at: {csv_filename}")
            print("Calculation failed")

if __name__ == "__main__":
    main()
