import os
import subprocess
import sys
import time

# For proper UTF-8 output (especially in Windows console)
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Parameters from previous steps
output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup6"
resolution = 0.9
csv_filename = f'grayscale_line_res{resolution}.csv'
csv_path = os.path.join(output_dir, csv_filename)

def run_py1_in_background():
    """Run py1.py in the background with the specified resolution."""
    # Compose the command
    cmd = [sys.executable, "py1.py", "-resolution", str(resolution)]
    try:
        # Run as a subprocess
        print(f"Running: {' '.join(cmd)}")
        proc = subprocess.Popen(cmd)
        # Optional: Wait for completion or poll for file existence
        max_wait = 60  # seconds
        waited = 0
        interval = 2
        while waited < max_wait:
            if os.path.exists(csv_path):
                print("Calculation successful")
                return True
            if proc.poll() is not None:
                # Process finished, break to check for file one last time
                break
            time.sleep(interval)
            waited += interval
        # Final check after process ends or timeout
        if os.path.exists(csv_path):
            print("Calculation successful")
            return True
        else:
            print(f"Calculation failed: {csv_path} not found after {max_wait} seconds.")
            return False
    except Exception as e:
        print(f"Error running py1.py: {e}")
        return False

def main():
    # Check if CSV already exists before running
    if os.path.exists(csv_path):
        print("Calculation successful")
        return
    # Otherwise, run py1.py and check
    run_py1_in_background()

if __name__ == '__main__':
    main()
