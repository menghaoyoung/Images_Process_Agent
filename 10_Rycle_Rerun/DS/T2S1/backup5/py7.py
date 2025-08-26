import os
import subprocess
import sys
import time

def run_program(script_name, args=None):
    """Execute a Python script and capture its output"""
    cmd = [sys.executable, script_name]
    if args:
        cmd.extend(args)
    
    print(f"\n{'='*60}")
    print(f"Executing: {script_name} {' '.join(args) if args else ''}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Errors in {script_name}:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Failed to execute {script_name}: {str(e)}")
        return False

def main():
    # Configuration
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup5"
    
    # Create output directory if missing
    os.makedirs(output_dir, exist_ok=True)
    
    # Pipeline execution sequence
    programs = [
        {"name": "py1.py", "args": ["-resolution=1.08"]},
        {"name": "py2.py", "args": None},
        {"name": "py3.py", "args": None},
        {"name": "py4.py", "args": None},
        {"name": "py5.py", "args": None}
    ]
    
    # Execute all programs in sequence
    print("\n" + "="*60)
    print("STARTING AUTOMATED ANALYSIS PIPELINE")
    print("="*60)
    
    all_success = True
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    log_file = os.path.join(output_dir, f"pipeline_log_{timestamp}.txt")
    
    with open(log_file, 'w') as log:
        log.write("Automated Pipeline Execution Log\n")
        log.write(f"Timestamp: {timestamp}\n")
        log.write("="*80 + "\n\n")
        
        for program in programs:
            success = run_program(program["name"], program["args"])
            log_entry = (
                f"\n{'='*60}\n"
                f"Program: {program['name']} {' '.join(program['args']) if program['args'] else ''}\n"
                f"Status: {'SUCCESS' if success else 'FAILURE'}\n"
                f"{'='*60}\n"
            )
            log.write(log_entry)
            
            if not success:
                all_success = False
                print(f"Pipeline failed at {program['name']}")
                break
    
    # Final status
    print("\n" + "="*60)
    if all_success:
        print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
    else:
        print("PIPELINE EXECUTION FAILED")
    
    print(f"Execution log saved to: {log_file}")
    print("="*60)

if __name__ == "__main__":
    main()
