import os
import subprocess
import time
import sys

def main():
    # Define parameters from task description
    resolution = 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup9"
    csv_filename = f"grayscale_values_res_{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    print(f"Running py1.py with resolution {resolution} in background...")
    
    try:
        # Run py1.py in background process
        process = subprocess.Popen([sys.executable, "py1.py"], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        
        # Wait for process to complete with timeout
        try:
            stdout, stderr = process.communicate(timeout=30)
            if process.returncode != 0:
                print(f"Error running py1.py. Exit code: {process.returncode}")
                if stderr:
                    print("Error output:")
                    print(stderr.decode())
                return
        except subprocess.TimeoutExpired:
            print("py1.py execution timed out")
            process.kill()
            return
        
        # Verify CSV file creation
        if os.path.exists(csv_path):
            print("Calculation successful")
            print(f"Output file created: {csv_path}")
        else:
            print(f"Error: CSV file not found at {csv_path}")
            print("Calculation failed")
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
