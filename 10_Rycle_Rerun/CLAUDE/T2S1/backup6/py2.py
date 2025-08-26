import os
import subprocess
import sys
import time

def run_and_verify():
    # Define the output directory and expected files for resolution 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup6"
    resolution = 1.08
    expected_csv = os.path.join(output_dir, f"line_grayscale_res_{resolution}.csv")
    expected_plot = os.path.join(output_dir, f"line_grayscale_plot_res_{resolution}.png")
    expected_npy = os.path.join(output_dir, f"line_grayscale_array_res_{resolution}.npy")
    
    print(f"Running py1.py with resolution={resolution}...")
    
    # Run the first program with the specified resolution in the background
    try:
        process = subprocess.Popen(["python", "py1.py", f"-resolution={resolution}"], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for the process to complete (optional timeout in seconds)
        timeout = 60
        start_time = time.time()
        while process.poll() is None:
            if time.time() - start_time > timeout:
                process.terminate()
                print(f"Process timed out after {timeout} seconds")
                return False
            time.sleep(0.5)
        
        # Get output and error messages
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"Error running py1.py: {stderr.decode('utf-8')}")
            return False
        else:
            print("py1.py completed successfully")
            
    except Exception as e:
        print(f"Error executing py1.py: {e}")
        return False
    
    # Check if files exist after running the program
    time.sleep(1)  # Small delay to ensure file system has updated
    
    files_exist = True
    if not os.path.exists(expected_csv):
        print(f"CSV file not found at: {expected_csv}")
        files_exist = False
    
    if not os.path.exists(expected_plot):
        print(f"Plot file not found at: {expected_plot}")
        files_exist = False
        
    if not os.path.exists(expected_npy):
        print(f"NumPy array file not found at: {expected_npy}")
        files_exist = False
    
    if files_exist:
        print("Calculation successful")
        
        # Display information about the CSV file
        try:
            file_size = os.path.getsize(expected_csv)
            print(f"CSV file size: {file_size} bytes")
            
            # Count lines in CSV file
            with open(expected_csv, 'r') as f:
                line_count = sum(1 for line in f)
            print(f"CSV file contains {line_count} lines (including header)")
            
        except Exception as e:
            print(f"Error getting file details: {e}")
        
        return True
    else:
        print("Calculation failed: One or more output files are missing")
        return False

if __name__ == "__main__":
    run_and_verify()
