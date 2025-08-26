import os
import subprocess
import sys

def fix_and_run_py1():
    # Path to the py1.py script
    py1_path = "py1.py"
    
    # Read the current content of py1.py
    try:
        with open(py1_path, 'r', encoding='utf-8') as f:
            content = f.readlines()
    except Exception as e:
        print(f"Error reading py1.py: {str(e)}")
        sys.exit(1)
    
    # Find and fix the import error
    fixed_content = []
    io_import_added = False
    for line in content:
        # Fix the problematic line
        if "sys.stdout = io.TextIOWrapper" in line:
            # Add the missing import io statement
            if not io_import_added:
                fixed_content.append("import io\n")
                io_import_added = True
        fixed_content.append(line)
    
    # Write the fixed content back to py1.py
    try:
        with open(py1_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_content)
        print("Successfully fixed import error in py1.py")
    except Exception as e:
        print(f"Error writing py1.py: {str(e)}")
        sys.exit(1)
    
    # Run the fixed py1.py with resolution 1.08
    resolution = 1.08
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup3"
    csv_filename = f"grayscale_values_{resolution:.2f}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    print(f"Running fixed py1.py with resolution={resolution}")
    try:
        command = ["python", py1_path, f"-resolution={resolution}"]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"py1.py execution failed: {str(e)}")
        sys.exit(1)
    
    # Verify CSV creation
    if os.path.exists(csv_path):
        print(f"CSV file created: {csv_path}")
        print("Calculation successful")
    else:
        print(f"Error: CSV file not found at {csv_path}")
        sys.exit(1)

if __name__ == '__main__':
    fix_and_run_py1()
