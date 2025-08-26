import os
import subprocess
import sys
import time

def run_py1_in_background(resolution=0.9):
    """
    Runs py1.py in the background with the given resolution argument.
    """
    # Prepare the command
    cmd = [sys.executable, "py1.py", "-resolution", str(resolution)]
    # Launch py1.py in the background
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc

def check_csv_exists(resolution=0.9):
    """
    Checks if the expected CSV file exists in the output directory.
    """
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup"
    csv_filename = f"line_grayscale_resolution_{resolution}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    return os.path.exists(csv_path)

def main():
    resolution = 0.9
    proc = run_py1_in_background(resolution=resolution)
    # Wait for process to finish (polling for completion and existence of the file)
    timeout_sec = 60
    poll_interval = 2
    waited = 0
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup"
    csv_filename = f"line_grayscale_resolution_{resolution}.csv"
    csv_path = os.path.join(output_dir, csv_filename)

    while waited < timeout_sec:
        if os.path.exists(csv_path):
            print("Calculation successful")
            break
        # Check if the process has finished
        if proc.poll() is not None:
            # Process finished; check one more time
            if os.path.exists(csv_path):
                print("Calculation successful")
            else:
                print("Calculation failed: CSV file not found.")
            break
        time.sleep(poll_interval)
        waited += poll_interval
    else:
        print("Timeout: CSV file not found after waiting.")

if __name__ == "__main__":
    main()
