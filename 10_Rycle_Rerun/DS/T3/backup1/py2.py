import os
import subprocess
import sys

def run_py1_and_verify():
    input_dir = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T3\backup1"
    
    # Step 1: Run py1.py in background
    print("Running image processing script...")
    process = subprocess.Popen([sys.executable, "py1.py"], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        print(f"Error running py1.py:\n{stderr.decode()}")
        return False
    
    # Step 2: Verify outputs
    print("Verifying output files...")
    valid_count = 0
    input_images = [f for f in os.listdir(input_dir) 
                   if f.lower().startswith("poly_") and 
                   f.lower().endswith(('.png', '.jpg'))]
    
    for img in input_images:
        base_name = os.path.splitext(img)[0]
        csv_file = f"{base_name}_gap_analysis.csv"
        png_file = f"{base_name}_gap.png"
        
        csv_exists = os.path.exists(os.path.join(output_dir, csv_file))
        png_exists = os.path.exists(os.path.join(output_dir, png_file))
        
        if csv_exists and png_exists:
            valid_count += 1
        else:
            missing = []
            if not csv_exists: missing.append(csv_file)
            if not png_exists: missing.append(png_file)
            print(f"Missing outputs for {img}: {', '.join(missing)}")
    
    # Final verification
    if valid_count == len(input_images):
        print("Calculation successful")
        return True
    else:
        print(f"Validation failed: {valid_count}/{len(input_images)} images processed successfully")
        return False

if __name__ == "__main__":
    run_py1_and_verify()
