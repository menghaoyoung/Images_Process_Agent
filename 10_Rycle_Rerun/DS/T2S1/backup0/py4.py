import subprocess
import os
import time

def main():
    # Define parameters
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup"
    resolution = 1.08
    csv_filename = f"grayscale_values_res_{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    # Run py1.py in the background
    command = ["python", "py1.py", f"-resolution={resolution}"]
    
    try:
        # Start the process in background
        process = subprocess.Popen(command, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        
        # Wait for process to complete with timeout
        print(f"Running py1.py with resolution={resolution}...")
        try:
            _, _ = process.communicate(timeout=30)  # 30-second timeout
            if process.returncode != 0:
                print(f"Error: py1.py exited with code {process.returncode}")
                return
        except subprocess.TimeoutExpired:
            print("Error: py1.py execution timed out")
            process.kill()
            return
        
        # Verify CSV creation
        if os.path.exists(csv_path):
            print("Calculation successful")
            print(f"Output CSV created: {csv_path}")
        else:
            print("Error: CSV file not created")
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
