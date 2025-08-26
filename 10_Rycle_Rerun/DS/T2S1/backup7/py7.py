import os
import subprocess
import time

def main():
    resolution = 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup7"
    csv_filename = f"grayscale_values_res_{resolution}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    # Run py1.py in background with specified resolution
    try:
        # Start the process in the background
        process = subprocess.Popen(
            ['python', 'py1.py', f'-resolution={resolution}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Started py1.py in background with resolution={resolution}")
        
        # Wait briefly to allow file creation
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print("Background process is still running...")
        
        # Wait for process to complete with timeout
        try:
            stdout, stderr = process.communicate(timeout=30)
            if stdout:
                print("Program output:")
                print(stdout)
            if stderr:
                print("Program errors:")
                print(stderr)
        except subprocess.TimeoutExpired:
            print("Process timed out after 30 seconds")
            process.kill()
        
    except Exception as e:
        print(f"Error running py1.py: {e}")
    
    # Verify if CSV files exist
    if os.path.exists(csv_path):
        print("\nCalculation successful")
        print(f"CSV file created: {csv_path}")
        # Additional verification - check if file has content
        if os.path.getsize(csv_path) > 0:
            print("File contains data - verification complete")
        else:
            print("Warning: File exists but is empty")
    else:
        print("\nCalculation failed - CSV file not found")
        print(f"Expected path: {csv_path}")
        # Check if directory exists
        if not os.path.exists(output_dir):
            print(f"Output directory missing: {output_dir}")
        else:
            print("Directory exists but file not found")

if __name__ == '__main__':
    main()
