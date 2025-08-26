import subprocess
import os
import sys

def main():
    resolution = 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup4"
    csv_filename = f"grayscale_values_{resolution}.csv"
    output_path = os.path.join(output_dir, csv_filename)
    
    print(f"Running py1.py with resolution={resolution} in foreground...")
    result = subprocess.run(
        ["python", "py1.py", f"-resolution={resolution}"],
        capture_output=True,
        text=True
    )
    
    print("\n=== STDOUT ===")
    print(result.stdout)
    
    print("\n=== STDERR ===")
    print(result.stderr)
    
    print("\n=== STATUS ===")
    if os.path.exists(output_path):
        print("Calculation successful")
        print(f"Output file: {output_path}")
    else:
        print("Calculation failed")
        print("Possible issues:")
        print("1. Image file not found at expected path")
        print("2. Invalid coordinates in line segment")
        print("3. File permission error in output directory")
        print("4. Errors in py1.py code (see above output)")
        
        # Check image path existence
        img_path = rf"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS\Li_{resolution}.png"
        if not os.path.exists(img_path):
            print(f"\nERROR: Image file not found - {img_path}")
        else:
            print(f"\nImage file exists: {img_path}")
            
        # Check output directory permissions
        if not os.access(output_dir, os.W_OK):
            print(f"\nERROR: No write permission in output directory - {output_dir}")

if __name__ == "__main__":
    main()
