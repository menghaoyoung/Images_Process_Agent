import os
import sys
import subprocess
import time

# Parameters from previous steps
start_point = (152, 29)
end_point = (136, 91)
resolution = 1.08
output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup7"

# Construct expected CSV file path based on naming in py1.py
csv_name = f"grayscale_line_{start_point[0]}_{start_point[1]}_{end_point[0]}_{end_point[1]}_res{resolution:.2f}.csv"
csv_path = os.path.join(output_dir, csv_name)

def run_py1_in_background():
    # Run py1.py in the background with the specified resolution
    # Note: On Windows, use 'python' command; adjust if needed for your python executable
    cmd = [sys.executable, "py1.py", "-resolution", str(resolution)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def main():
    print(f"Running py1.py in the background with resolution={resolution}...")
    process = run_py1_in_background()
    # Wait for process to finish (but could also poll for the file if preferred)
    stdout, stderr = process.communicate()
    # Optionally print output for debugging
    print(stdout.decode('utf-8'))
    if process.returncode != 0:
        print("py1.py failed to run:")
        print(stderr.decode('utf-8'))
        sys.exit(1)

    # Check if CSV file exists
    if os.path.exists(csv_path):
        print("Calculation successful")
    else:
        print(f"CSV file was not created: {csv_path}")

if __name__ == "__main__":
    main()
