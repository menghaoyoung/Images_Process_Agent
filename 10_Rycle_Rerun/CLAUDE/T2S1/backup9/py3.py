import os
import subprocess
import sys
import time

def verify_output_files():
    # Define the resolution
    resolution = 1.08
    
    # Define output directory
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup9"
    
    # Define expected CSV file path
    csv_file = os.path.join(output_dir, f"line_grayscale_res_{resolution}.csv")
    
    # Run the first script with the required resolution parameter
    print(f"Running py1.py with resolution={resolution} in the background...")
    
    try:
        # Start the process in the background
        process = subprocess.Popen([sys.executable, "py1.py", f"-resolution={resolution}"], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("Process started. Waiting for completion...")
        
        # Wait for a few seconds to allow the process to complete
        max_wait_time = 30  # seconds
        wait_interval = 2   # seconds
        total_waited = 0
        
        while process.poll() is None and total_waited < max_wait_time:
            time.sleep(wait_interval)
            total_waited += wait_interval
            print(f"Still waiting... ({total_waited} seconds)")
        
        # Check if the process is still running
        if process.poll() is None:
            print("Process is taking too long. Continuing anyway...")
        else:
            stdout, stderr = process.communicate()
            if stdout:
                print("Command output summary:")
                print(stdout[:200] + "..." if len(stdout) > 200 else stdout)
            
            if stderr:
                print("Command errors:")
                print(stderr)
    
        # Check if the CSV file exists
        if os.path.exists(csv_file):
            print("Calculation successful")
            
            # Get file size and modification time
            file_size = os.path.getsize(csv_file)
            mod_time = os.path.getmtime(csv_file)
            mod_time_str = time.ctime(mod_time)
            
            print(f"CSV file found at: {csv_file}")
            print(f"File size: {file_size} bytes")
            print(f"Last modified: {mod_time_str}")
            
            # Optionally read the first few lines of the CSV file
            try:
                with open(csv_file, 'r') as f:
                    header = f.readline().strip()
                    first_line = f.readline().strip()
                    print(f"CSV header: {header}")
                    print(f"First data row: {first_line}")
            except Exception as e:
                print(f"Could not read CSV file: {str(e)}")
        else:
            print("Calculation failed")
            print(f"CSV file not found at: {csv_file}")
    
    except Exception as e:
        print(f"Error running py1.py: {str(e)}")

if __name__ == "__main__":
    verify_output_files()
