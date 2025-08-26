import os
import subprocess
import time

def main():
    # Define the output directory and expected CSV filename
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup1"
    output_csv = os.path.join(output_dir, "line_grayscale_values.csv")

    # Run py1.py in the background for resolution=0.9
    # The image path and other params match those from previous steps
    command = [
        "python", "py1.py",
        "-resolution", "0.9",
        "-image_dir", r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png",
        "-output_dir", output_dir,
        "-start_point", "152,29",
        "-end_point", "136,91"
    ]
    print("Running py1.py in the background ...")
    proc = subprocess.Popen(command)

    # Wait for the process to finish
    while proc.poll() is None:
        time.sleep(1)  # Wait 1 second between checks

    # After process completion, check if CSV exists
    if os.path.isfile(output_csv):
        print("Calculation successful")
    else:
        print("Calculation failed: CSV file not found.")

if __name__ == "__main__":
    main()
