import os
import subprocess
import time

def main():
    # Parameters
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup3"
    resolution = 0.9
    csv_filename = f'grayscale_and_μeq_res{resolution}.csv'
    csv_path = os.path.join(output_dir, csv_filename)

    # Build command to run py1.py in the background with resolution=0.9
    # Note: For maximum compatibility, use sys.executable to get Python path if needed
    py1_path = "py1.py"

    # If output file exists from earlier, remove it
    if os.path.exists(csv_path):
        os.remove(csv_path)

    # Start the process
    process = subprocess.Popen(
        ["python", py1_path, "-resolution", str(resolution)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for process to finish (or poll for file creation)
    timeout = 60  # seconds
    poll_interval = 1
    elapsed = 0
    while elapsed < timeout:
        if os.path.exists(csv_path):
            print("Calculation successful")
            break
        # Check if process has exited and still no file
        if process.poll() is not None:
            # Process ended
            if os.path.exists(csv_path):
                print("Calculation successful")
            else:
                # Print error from process
                out, err = process.communicate()
                print("Process ended but file not found.")
                print("STDOUT:\n", out.decode())
                print("STDERR:\n", err.decode())
            break
        time.sleep(poll_interval)
        elapsed += poll_interval
    else:
        print("Timeout: CSV file was not created within expected time.")

if __name__ == "__main__":
    main()
