import os
import sys

def main():
    resolution = 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup4"
    csv_filename = f"grayscale_values_{resolution}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    if os.path.exists(csv_path):
        print("Calculation successful")
        sys.exit(0)
    else:
        print(f"Error: CSV file not found at {csv_path}")
        print("Please run py1.py with resolution=1.08 first")
        sys.exit(1)

if __name__ == "__main__":
    main()
