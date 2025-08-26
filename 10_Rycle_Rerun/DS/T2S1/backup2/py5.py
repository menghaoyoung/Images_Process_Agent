import os
import subprocess
import time
import sys

def main():
    # Fixed parameters matching py1.py
    resolution = 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup2"
    csv_filename = f"grayscale_values_res_{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    # Remove existing CSV file if present (to ensure fresh test)
    if os.path.exists(csv_path):
        try:
            os.remove(csv_path)
            print(f"Removed existing file: {csv_path}")
        except Exception as e:
            print(f"Error removing file: {e}")
            sys.exit(1)
    
    # Run py1.py in background with resolution argument
    cmd = f'python py1.py -resolution={resolution}'
    print(f"Executing: {cmd}")
    process = subprocess.Popen(cmd, shell=True)
    
    # Monitor for file creation with timeout
    timeout = 10  # seconds
    start_time = time.time()
    file_created = False
    
    while (time.time() - start_time) < timeout:
        if os.path.exists(csv_path):
            file_created = True
            break
        time.sleep(0.5)  # Check every half second
    
    # Verify and report results
    if file_created:
        file_size = os.path.getsize(csv_path)
        print(f"CSV file created: {csv_path}")
        print(f"File size: {file_size} bytes")
        print("Calculation successful")
    else:
        print(f"Error: CSV file not created after {timeout} seconds")
        print("Calculation failed")
        
        # Check process status
        if process.poll() is None:
            print("Process still running - terminating...")
            process.terminate()
        else:
            print(f"Process exited with code: {process.returncode}")

if __name__ == "__main__":
    main()
