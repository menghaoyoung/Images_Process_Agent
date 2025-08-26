# py2.py - Verify output files from py1.py
import os

def verify_output():
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup4"
    enhanced_directory = os.path.join(output_directory, "enhanced")
    csv_directory = os.path.join(output_directory, "csv")
    result_image_directory = os.path.join(output_directory, "result_images")
    
    # Check if directories exist
    directories_exist = True
    for directory in [output_directory, enhanced_directory, csv_directory, result_image_directory]:
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            directories_exist = False
    
    if not directories_exist:
        return False
    
    # Check for CSV files
    csv_files = [f for f in os.listdir(csv_directory) if f.endswith('_gap_analysis.csv')]
    print(f"Found {len(csv_files)} CSV files")
    
    # Check for result images
    result_images = [f for f in os.listdir(result_image_directory) if f.endswith('_gap_result.png')]
    print(f"Found {len(result_images)} result images")
    
    # Check for enhanced images
    enhanced_images = [f for f in os.listdir(enhanced_directory) if f.endswith('_enhanced.png')]
    print(f"Found {len(enhanced_images)} enhanced images")
    
    # Verify that we have the expected number of files (5 of each type)
    if len(csv_files) == 5 and len(result_images) == 5 and len(enhanced_images) == 5:
        print("Calculation successful")
        return True
    else:
        print("Missing some output files")
        return False

if __name__ == "__main__":
    verify_output()
