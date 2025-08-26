import os
import subprocess
import time

def main():
    # Set parameters according to the task description
    resolution = 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup9"
    output_filename = f'line_grayscale_values_res{resolution:.2f}.csv'
    output_path = os.path.join(output_dir, output_filename)

    # Run py1.py in the background with required resolution argument
    # The command assumes py1.py is in the current directory
    # For Windows, use 'python' command
    print("Starting py1.py in the background...")
    process = subprocess.Popen(
        ['python', 'py1.py', '-resolution', str(resolution)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for the process to finish
    stdout, stderr = process.communicate()
    print(stdout.decode('utf-8'))
    if stderr:
        print("Errors:")
        print(stderr.decode('utf-8'))

    # Check if the output CSV exists
    if os.path.exists(output_path):
        print("Calculation successful")
    else:
        print("Calculation failed: CSV file not found.")

if __name__ == "__main__":
    main()
