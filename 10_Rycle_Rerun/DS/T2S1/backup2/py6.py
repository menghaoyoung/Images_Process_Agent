import os
import subprocess
import time
import sys

def main():
    # Fixed parameters matching py1.py
    resolution = 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup2"
    csv_filename = f"grayscale_values_res_{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Remove existing CSV if present
    if os.path.exists(csv_path):
        try:
            os.remove(csv_path)
            print(f"Removed existing file: {csv_path}")
        except Exception as e:
            print(f"Warning: Could not remove existing file - {e}")
    
    # Use full path to Python executable to avoid 9009 error
    python_exe = sys.executable
    
    # Build command with explicit Python path
    cmd = f'"{python_exe}" py1.py -resolution={resolution}'
    print(f"Executing: {cmd}")
    
    # Run py1.py and wait for completion
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait with timeout
        try:
            stdout, stderr = process.communicate(timeout=15)
            return_code = process.returncode
            
            # Print captured output
            print("Program output:")
            print(stdout.decode('utf-8', errors='replace'))
            if stderr:
                print("Program errors:")
                print(stderr.decode('utf-8', errors='replace'))
                
        except subprocess.TimeoutExpired:
            process.terminate()
            print("ERROR: Program execution timed out after 15 seconds")
            return_code = -1
        
    except Exception as e:
        print(f"FATAL ERROR: Could not execute program - {e}")
        return_code = -2
    
    # Verify CSV creation
    if os.path.exists(csv_path):
        try:
            with open(csv_path) as f:
                line_count = sum(1 for _ in f)
            print(f"CSV file created: {csv_path}")
            print(f"Contains {line_count} data points")
            print("Calculation successful")
            sys.exit(0)
        except Exception as e:
            print(f"ERROR: Problem with CSV file - {e}")
            sys.exit(3)
    else:
        print(f"ERROR: CSV file not created at {csv_path}")
        print(f"Program exited with code: {return_code}")
        
        # Provide troubleshooting tips
        print("\nTROUBLESHOOTING:")
        print("1. Verify py1.py exists in current directory")
        print("2. Check the image path in py1.py is correct")
        print("3. Ensure the output directory is accessible")
        print("4. Review py1.py for runtime errors")
        
        sys.exit(1)

if __name__ == "__main__":
    main()
