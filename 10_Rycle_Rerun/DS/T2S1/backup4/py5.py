import os
import subprocess
import sys
import time

def main():
    resolution = 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup4"
    csv_filename = f"grayscale_values_{resolution}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    print(f"Running py1.py with resolution={resolution}...")
    result = subprocess.run(
        ["python", "py1.py", f"-resolution={resolution}"],
        capture_output=True,
        text=True
    )
    
    # Print output for debugging
    print("\n=== py1.py OUTPUT ===")
    print(result.stdout)
    if result.stderr:
        print("\n=== ERRORS ===")
        print(result.stderr)
    
    # Verify CSV creation
    print("\n=== VERIFICATION ===")
    if os.path.exists(csv_path):
        print("Calculation successful")
        print(f"CSV file created: {csv_path}")
        
        # Additional validation: check CSV contents
        try:
            with open(csv_path, 'r') as f:
                lines = f.readlines()
                if len(lines) > 0:
                    print(f"CSV contains {len(lines)} grayscale values")
                    print("First 5 values:", ', '.join(lines[:5]).strip())
                else:
                    print("Warning: CSV file is empty")
        except Exception as e:
            print(f"Error reading CSV: {str(e)}")
    else:
        print("Calculation failed")
        print(f"CSV file not found at: {csv_path}")
        print("Possible reasons:")
        print("- py1.py encountered an error (see output above)")
        print("- Incorrect output path configuration")
        print("- File permission issues")

if __name__ == "__main__":
    main()
