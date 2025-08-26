import os
import shutil

def main():
    # Source image (1.0 resolution)
    src_dir = r"C:\Users\admin\Desktop\Python_proj\datas\T2_IMGS"
    src_image = "Li_1.0.png"
    src_path = os.path.join(src_dir, src_image)
    
    # Target image (1.08 resolution)
    target_res = 1.08
    target_image = f"Li_{target_res}.png"
    target_path = os.path.join(src_dir, target_image)
    
    # Create backup directory for results
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup4"
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if source image exists
    if not os.path.exists(src_path):
        print(f"Error: Source image not found at {src_path}")
        return
    
    # Create the 1.08 resolution image
    try:
        shutil.copy2(src_path, target_path)
        print(f"Created image: {target_path}")
        print("You can now run py1.py with resolution=1.08")
    except Exception as e:
        print(f"Error creating image: {str(e)}")
        # Fallback: create symbolic link if copy fails
        try:
            if os.name == 'nt':  # Windows
                import ctypes
                ctypes.windll.kernel32.CreateSymbolicLinkW(target_path, src_path, 0)
            else:  # Unix
                os.symlink(src_path, target_path)
            print(f"Created symbolic link: {target_path} -> {src_path}")
        except Exception as sym_e:
            print(f"Failed to create symbolic link: {str(sym_e)}")

if __name__ == "__main__":
    main()
