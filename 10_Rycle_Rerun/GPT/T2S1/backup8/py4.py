import os
import subprocess
import time

def main():
    # Configuration
    script_name = "py1.py"
    resolution = 1.08
    image_path = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_1.0.png"
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\GPT\T2S1\backup8"
    start_point = "152,29"
    end_point = "136,91"

    # The expected CSV file name (must match naming in py1.py)
    img_name = os.path.splitext(os.path.basename(image_path))[0]
    csv_file = f"{img_name}_line_152_29_136_91_res{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_file)

    # Run py1.py in the background with the correct arguments
    command = [
        "python", script_name,
        "-resolution", str(resolution),
        "-image_dir", image_path,
        "-output_dir", output_dir,
        "-start", start_point,
        "-end", end_point
    ]

    print("Running py1.py in the background...")
    process = subprocess.Popen(command)

    # Wait for the process to finish (alternatively, sleep and check for file)
    process.wait(timeout=120)  # waits up to 2 minutes

    # Check if the CSV file exists
    if os.path.exists(csv_path):
        print("Calculation successful")
    else:
        print("Calculation failed: CSV file does not exist.")

if __name__ == "__main__":
    main()
