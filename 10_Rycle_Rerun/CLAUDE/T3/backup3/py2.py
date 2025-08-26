import os
import glob

def verify_output():
    # Define the output directory path
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup3"
    
    # Check if the directory exists
    if not os.path.exists(output_directory):
        print(f"Output directory {output_directory} does not exist!")
        return False
    
    # Get lists of the output files
    csv_files = glob.glob(os.path.join(output_directory, "*_gap_analysis.csv"))
    enhanced_images = glob.glob(os.path.join(output_directory, "*_enhanced.png"))
    result_images = glob.glob(os.path.join(output_directory, "*_gap_result.png"))
    
    # Count the files
    csv_count = len(csv_files)
    enhanced_count = len(enhanced_images)
    result_count = len(result_images)
    
    print(f"Found {csv_count} CSV files, {enhanced_count} enhanced images, and {result_count} result images.")
    
    # Check if we have output files for all 5 processed images
    expected_file_count = 5  # Based on the previous output showing 5 Poly_*.png files processed
    
    if csv_count >= expected_file_count and result_count >= expected_file_count:
        print("Calculation successful")
        return True
    else:
        print("Some output files are missing!")
        return False

if __name__ == "__main__":
    verify_output()
