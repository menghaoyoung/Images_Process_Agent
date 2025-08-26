import os
import subprocess
import sys
import time

def main():
    # Fixed parameters from previous program
    resolution = 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup3"
    csv_filename = f"grayscale_values_{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    # Run py1.py in background with specified resolution
    try:
        # Start the process in background (detached)
        command = ["python", "py1.py", f"-resolution={resolution}"]
        
        # Platform-specific creation flags
        if sys.platform == "win32":
            creation_flags = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
            subprocess.Popen(command, 
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             creationflags=creation_flags)
        else:  # Unix-based systems
            subprocess.Popen(command, 
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             start_new_session=True)
        
        print(f"Started py1.py in background with resolution={resolution}")
        
        # Wait for process to complete with periodic checks
        max_wait_time = 30  # seconds
        check_interval = 0.5  # seconds
        elapsed = 0
        
        while elapsed < max_wait_time:
            if os.path.exists(csv_path):
                print("Calculation successful")
                return
            time.sleep(check_interval)
            elapsed += check_interval
        
        # If we reach here, CSV wasn't created in time
        print("Error: CSV file not created within timeout period")
    
    except Exception as e:
        print(f"Error running verification: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
