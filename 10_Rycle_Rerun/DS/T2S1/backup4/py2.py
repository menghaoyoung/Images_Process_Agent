import subprocess
import os
import time
import sys

def main():
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup4"
    resolution = 1.08
    csv_filename = f"grayscale_values_{resolution}.csv"
    output_path = os.path.join(output_dir, csv_filename)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Run py1.py with specified resolution in the background
    command = ["python", "py1.py", f"-resolution={resolution}"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Display status message
    print(f"Running py1.py for resolution {resolution} in background (PID: {process.pid})...")
    
    # Continuously check for file existence
    max_attempts = 30
    for attempt in range(max_attempts):
        time.sleep(0.5)  # Check every 500ms
        
        if os.path.exists(output_path):
            print("Calculation successful")
            return
            
    print(f"Calculation failed: {csv_filename} not found after {max_attempts*0.5}s")

if __name__ == "__main__":
    main()
