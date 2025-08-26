import os
import subprocess
import time
import sys

def main():
    # Define parameters
    resolution = 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup5"
    filename = f"grayscale_values_res_{str(resolution).replace('.', '_')}.csv"
    output_path = os.path.join(output_dir, filename)
    
    # Run py1.py in background with specified resolution
    cmd = [sys.executable, "py1.py", f"-resolution={resolution}"]
    subprocess.Popen(cmd)
    
    # Wait and verify CSV creation
    max_attempts = 10
    for _ in range(max_attempts):
        time.sleep(0.5)  # Check every 0.5 seconds
        if os.path.exists(output_path):
            print("Calculation successful")
            return
    
    print("Error: CSV file not found after execution")

if __name__ == "__main__":
    main()
