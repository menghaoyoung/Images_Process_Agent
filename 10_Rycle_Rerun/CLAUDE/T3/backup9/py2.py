import os
import glob

def verify_outputs():
    output_directory = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\CLAUDE\T3\backup9"
    input_directory = r"C:\Users\admin\Desktop\Python_proj\distance_analysis_new\Images"
    
    # Get all image files with "Poly_" prefix from the input directory
    image_files = [f for f in os.listdir(input_directory) 
                  if f.startswith("Poly_") and (f.lower().endswith(".png") or f.lower().endswith(".jpg"))]
    
    all_files_exist = True
    
    for image_file in image_files:
        base_name = os.path.splitext(image_file)[0]
        
        # Check if enhanced image exists
        enhanced_path = os.path.join(output_directory, f"{base_name}_enhanced.png")
        if not os.path.exists(enhanced_path):
            print(f"Missing enhanced image: {enhanced_path}")
            all_files_exist = False
        
        # Check if CSV file exists
        csv_path = os.path.join(output_directory, f"{base_name}_gap_analysis.csv")
        if not os.path.exists(csv_path):
            print(f"Missing CSV file: {csv_path}")
            all_files_exist = False
        
        # Check if highlighted image exists
        highlight_path = os.path.join(output_directory, f"{base_name}_gap_highlighted.png")
        if not os.path.exists(highlight_path):
            print(f"Missing highlighted image: {highlight_path}")
            all_files_exist = False
    
    if all_files_exist:
        print("Calculation successful")
    else:
        print("Some files are missing")

if __name__ == "__main__":
    verify_outputs()
