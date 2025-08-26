import subprocess
import os
import time

def main():
    # Define parameters
    resolution = "1.08"
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup8"
    csv_filename = f"line_gray_values_res_{resolution}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    # Run py1.py in the background with specified resolution
    cmd = f'start /B python py1.py -resolution={resolution}'
    subprocess.run(cmd, shell=True)
    
    # Allow time for file creation
    time.sleep(2)
    
    # Verify if CSV file exists
    if os.path.exists(csv_path):
        print("Calculation successful")
    else:
        print("Calculation failed: CSV file not found")

if __name__ == "__main__":
    main()
