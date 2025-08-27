import os
import subprocess
import sys

def verify_output_files(input_dir, output_dir):
    """Check if output CSV and PNG files exist for all processed images"""
    valid_extensions = ('.png', '.jpg', '.jpeg')
    img_count = 0
    success_count = 0
    
    for filename in os.listdir(input_dir):
        if not filename.startswith("Poly_"):
            continue
        if not filename.lower().endswith(valid_extensions):
            continue
            
        img_count += 1
        base_name = os.path.splitext(filename)[0]
        csv_file = os.path.join(output_dir, f"{base_name}_gap_analysis.csv")
        png_file = os.path.join(output_dir, f"{base_name}_gap_mask.png")
        
        if os.path.exists(csv_file) and os.path.exists(png_file):
            success_count += 1
        else:
            print(f"Missing output for {filename}:")
            if not os.path.exists(csv_file): 
                print(f"  - CSV file not found: {csv_file}")
            if not os.path.exists(png_file): 
                print(f"  - PNG file not found: {png_file}")
    
    return img_count, success_count

if __name__ == "__main__":
    # Configure paths (match py1.py configuration)
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T3\backup8"
    
    # Run py1.py as subprocess
    print("Running py1.py...")
    result = subprocess.run(
        [sys.executable, "py1.py", input_directory],
        capture_output=True,
        text=True
    )
    
    # Display execution output
    if result.stdout:
        print("py1.py output:")
        print(result.stdout)
    if result.stderr:
        print("py1.py errors:")
        print(result.stderr)
    
    # Verify outputs
    print("\nVerifying output files...")
    total, success = verify_output_files(input_directory, output_directory)
    
    # Generate final status
    if total == 0:
        print("No valid input images found")
    elif success == total:
        print("\nCalculation successful")
    else:
        print(f"\nPartial success: {success}/{total} images processed")
