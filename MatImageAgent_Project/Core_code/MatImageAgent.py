import os
import re
import sys
import argparse
import subprocess
from openai import OpenAI

# Some Api configs
CONFIG = {
    'api_base': '',
    'api_key': '',
    'model': '',
    'max_tokens': 8192,
    'error_limit': 5,
    'pyfile_limit': 12,
    'encoding': 'UTF-8'
}

class ScriptExecutor:
    def __init__(self):
        self.client = OpenAI(
            base_url=CONFIG['api_base'],
            api_key=CONFIG['api_key']
        )
        self.conversation = []
        self.N_py = 1
        self.kk = 0

    def get_file_names(self):
        """Get file names in current directory"""
        files_and_dirs = os.listdir('.')
        files = [f for f in files_and_dirs if os.path.isfile(f)]
        return ' '.join(files)

    @staticmethod
    def pystr_extract(str1):
        """Extract Python code block from text"""
        match = re.search(r'```python\n(.*?)```', str1, re.DOTALL | re.IGNORECASE)
        return match.group(1) if match else "No Python code found."

    @staticmethod
    def pynotrun_check(str1):
        """Check if code execution is not required"""
        return re.search(r'NO-RUN-PY', str1, re.DOTALL | re.IGNORECASE)

    def execute_script(self, pystr):
        """Execute Python script and return output and errors"""
        filename = f"py{self.N_py}.py"
        with open(filename, "w", encoding=CONFIG['encoding']) as f:
            f.write(pystr)

        process = subprocess.Popen(
            ["python", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process.communicate()

    def call_gpt_api(self, messages):
        """Call LLM API"""
        response = self.client.chat.completions.create(
            model=CONFIG['model'],
            messages=messages,
            max_tokens=CONFIG['max_tokens'],
            temperature=0.7,
            stream=False
        )
        return response.choices[0].message.content

    def error_check(self, error):
        """Handle execution errors"""
        k_error = 0
        while error and k_error < CONFIG['error_limit']:
            print(f"Error: {error}")
            Str_header = f"The previous program contained errors. [Error Details: {error}] Please rectify these issues and submit a corrected, complete, and executable program precisely tailored to the subtask requirements."
            
            self.conversation.append({"role": "user", "content": Str_header})
            str1 = self.call_gpt_api(self.conversation)
            
            print('##### correction:\n', str1)
            self.conversation.append({"role": "assistant", "content": str1})

            str_py1 = self.pystr_extract(str1)
            if str_py1 == "No Python code found.":
                print('Mission complete.')
                sys.exit()

            print(f'Begin to execute Python {k_error}')
            output, error = self.execute_script(str_py1)
            print(error, k_error, self.N_py)
            
            self.N_py += 1
            if self.N_py > CONFIG['pyfile_limit']:
                print('Mission failed.')
                sys.exit()
            
            k_error += 1

        return error

    def process_task(self, code_str):
        """Process main task"""
        print('Mission Start')
        output = ""
        files_str = ""
        
        while True:
            if self.kk > 0:
                Str_header = "Start writing the second or third program, or skip if all tasks have been completed. Follow these requirements: (1) Output a complete and executable program strictly adhering to the task instructions, avoiding sample programs. (2) Consider the output of the previous step and the file names in the current directory, as they may result from the previous program and could be utilized in writing the current program. [Previous Step Output]:"
                CONTENT = Str_header + output + ".[Current directory file names]:" + files_str + ". [previous Task Description]:" + code_str
            else:
                Str_header = "Please carefully review the task description below. You will need to create two to three Python programs. Start by crafting the first Python program to meet the following criteria: (1) Ensure the program is complete and executable, tailored precisely to the task's requirements. (2) Include print statements to display output results, aiding in subsequent tasks. Keep this in mind. (3) Begin your Python code with '```python\n' and end with '```'. (4) Check whether the program requires execution. If not, include the statement 'NO-RUN-PY' in your response.[Task Description]:"
                CONTENT = Str_header + code_str

            self.conversation.append({"role": "user", "content": CONTENT})
            str1 = self.call_gpt_api(self.conversation)
            
            print('##### answer:\n', str1)
            self.conversation.append({"role": "assistant", "content": str1})

            str_py1 = self.pystr_extract(str1)
            if str_py1 == "No Python code found.":
                print('Mission complete.')
                break

            if self.pynotrun_check(str1):
                with open(f"py{self.N_py}.py", "w", encoding=CONFIG['encoding']) as f:
                    f.write(str_py1)
                output = " "
                files_str = " "
            else:
                print('Begin to execute Python')
                output, error = self.execute_script(str_py1)
                error = self.error_check(error)
                if error:
                    continue

            self.N_py += 1
            if self.N_py > CONFIG['pyfile_limit']:
                print('Mission failed.')
                break

            files_str = self.get_file_names()
            print(f'Step {self.kk+1} is finished')
            self.kk += 1

        print('Mission Complete')

def main():
    parser = argparse.ArgumentParser(description='Process some file.')
    parser.add_argument('-s', metavar='filename', type=str, help='the name of the file or string to process')
    args = parser.parse_args()
    
    if args.s.endswith(".txt") and ' ' not in args.s:
        with open(args.s, "r", encoding=CONFIG['encoding']) as file:
            code_str = file.read()
    else:
        code_str = args.s

    executor = ScriptExecutor()
    executor.process_task(code_str)

if __name__ == "__main__":
    main()