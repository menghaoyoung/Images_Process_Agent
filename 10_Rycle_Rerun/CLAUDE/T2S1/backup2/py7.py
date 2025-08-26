# py2.py - Run py1.py in the background and verify CSV file existence
import os
import subprocess
import time

def main():
    # Define the resolution to use
    resolution = 1.08
    
    # Define the output directory where CSV files will be saved
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup2"
    
    # Define the expected CSV file path
    expected_csv = os.path.join(output_dir, f"line_grayscale_res_{resolution}.csv")
    
    # Run py1.py in the background
    print(f"Running py1.py with resolution = {resolution} in the background...")
    
    # Start the process in the background
    process = subprocess.Popen(["python", "py1.py", f"-resolution={resolution}"])
    
    # Wait a bit to give the process time to start and potentially finish
    print("Waiting for the calculation to complete...")
    time.sleep(5)  # Adjust this time as needed
    
    # Check if the process is still running
    if process.poll() is None:
        print("The calculation is still running. Waiting longer...")
        # Wait for the process to complete
        process.wait()
    
    # Check if the CSV file exists
    if os.path.isfile(expected_csv):
        print("Calculation successful")
    else:
        print(f"CSV file not found: {expected_csv}")
        # If file not found, check if the process completed successfully
        if process.returncode != 0:
            print(f"py1.py exited with error code: {process.returncode}")

if __name__ == "__main__":
    main()
