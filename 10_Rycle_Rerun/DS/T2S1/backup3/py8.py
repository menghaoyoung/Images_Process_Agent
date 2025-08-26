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
    
    print(f"Starting processing with resolution: {resolution}")
    print(f"Expected CSV path: {csv_path}")
    
    # Run py1.py as a foreground process to capture output
    try:
        command = ["python", "py1.py", f"-resolution={resolution}"]
        
        # Execute and capture output in real-time
        print("\n--- Starting py1.py execution ---")
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   universal_newlines=True)
        
        # Stream output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Check exit code
        exit_code = process.poll()
        if exit_code != 0:
            print(f"\nError: py1.py exited with code {exit_code}")
            print("Please check the output above for errors")
            sys.exit(1)
        
        # Verify CSV creation
        max_wait_time = 60  # Increased to 60 seconds
        check_interval = 1  # Check every second
        elapsed = 0
        
        print("\n--- Verifying CSV creation ---")
        while elapsed < max_wait_time:
            if os.path.exists(csv_path):
                file_size = os.path.getsize(csv_path)
                print(f"CSV file found! Size: {file_size} bytes")
                print("Calculation successful")
                return
            print(f"Waiting for CSV... ({elapsed}/{max_wait_time}s)")
            time.sleep(check_interval)
            elapsed += check_interval
        
        # If we reach here, CSV wasn't created
        print("\nError: CSV file not created after 60 seconds")
        print("Possible reasons:")
        print("1. py1.py failed to create the CSV file")
        print("2. Incorrect output directory in py1.py")
        print("3. File permission issues")
        print("4. Disk full or storage problem")
        print(f"Please verify output directory: {output_dir}")
        
        # Check if directory exists
        if not os.path.exists(output_dir):
            print("ERROR: Output directory does not exist!")
            print("Creating directory now...")
            os.makedirs(output_dir, exist_ok=True)
            print("Please run py1.py again to generate CSV")
    
    except Exception as e:
        print(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
