import os
import subprocess
import sys
import time

def check_files_exist():
    # Define the output directory
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T2S1\backup8"
    
    # Define the resolution
    resolution = 1.08
    resolution_str = str(resolution).replace('.', '_')
    
    # Define expected files
    csv_file = os.path.join(output_dir, f"line_grayscale_res{resolution_str}.csv")
    npy_file = os.path.join(output_dir, f"line_grayscale_res{resolution_str}.npy")
    plot_file = os.path.join(output_dir, f"line_grayscale_plot_res{resolution_str}.png")
    
    # Run the first script with the specified resolution
    print(f"Running py1.py with resolution={resolution}...")
    try:
        # Run the script in the background
        process = subprocess.Popen(["python", "py1.py", f"-resolution={resolution}"], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
        
        # Wait for a short time to let the process start
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print("Script is running in the background...")
        
        # Wait for the process to complete (with timeout)
        try:
            stdout, stderr = process.communicate(timeout=30)
            print("Script execution completed.")
            if stderr:
                print(f"Errors: {stderr.decode('utf-8')}")
        except subprocess.TimeoutExpired:
            print("Script is taking too long, but continuing with file check...")
    
    except Exception as e:
        print(f"Error running script: {e}")
        return False
    
    # Give some time for files to be saved
    time.sleep(3)
    
    # Check if files exist
    files_exist = True
    for file_path, file_type in [
        (csv_file, "CSV file"),
        (npy_file, "NumPy array file"),
        (plot_file, "Plot image")
    ]:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"{file_type} exists: {file_path} (Size: {file_size} bytes)")
        else:
            print(f"{file_type} does not exist: {file_path}")
            files_exist = False
    
    return files_exist

if __name__ == "__main__":
    print("Starting verification process...")
    if check_files_exist():
        print("Calculation successful")
    else:
        print("Calculation failed or files not found")
