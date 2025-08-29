# MatImageAgent - Materials Characterization Image Processing Multimodal Agent

![MyWorkflow](https://github.com/menghaoyoung/Images_Process_Agent/raw/main/workflow.png)

This repository hosts the code and supporting materials for **MatImageAgent**, a Large Language Model (LLM)-based multimodal agent designed to automate image analysis workflows in solid-state battery materials research. MatImageAgent enables end-to-end automation of scanning electron microscopy (SEM), X-ray computed tomography (XCT), and atomic force microscopy (AFM) image processing—covering image recognition, quantitative analysis, and research report generation—without requiring researchers to master complex programming skills.

## 1. About MatImageAgent

MatImageAgent leverages prompt engineering and LLM API automation to execute materials image analysis tasks guided by a human-defined **Mission Description (MD)**. Its core workflow replaces repetitive manual operations (e.g., SEM void measurement, XCT grayscale mapping, AFM phase marking) with automated processes, achieving full coverage of the research pipeline:

`Image Input → Program Generation → Automated Processing → Data Analysis → Report Output`

We demonstrated 3 examples in our research:



*   **SEM Image Processing (TASK 1)**: Identify lithium striped voids and measure their height.

*   **XCT Image Processing (TASK 2)**: Extract grayscale values, map 8-bit to 16-bit dynamic range, and analyze lithium deposition.

*   **AFM Image Processing (TASK 3)**: Mark micro-phases (bright domains) and macro-phases (dark domains) of polymer films.

### 1.1 Paper Information

Waiting for updating

## 2. Writing the Mission Description (MD)

The **Mission Description (MD)** is a text file (`.txt`) that defines the image analysis task for MatImageAgent. It must be manually crafted by researchers and saved in the same directory as the agent code. To ensure high task completion quality, the MD should include **detailed, unambiguous instructions** for the following:

### Required MD Content



| Category             | Description                                                            | Example (TASK 1: SEM Void Analysis)                                                                                                      |
| -------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Task Objective       | Clear goal of the image analysis                                       | "Identify lithium striped voids in SEM images and calculate their maximum height."                                                       |
| Image Specifications | image type and input path                                              | "SEM images of Li/SEs interface (resolution = 0.1 μm/pixel) stored in `./Input_Images/SEM/`."                                            |
| Analysis Parameters  | Rules for target recognition | "Void pixels: grayscale 5–30; at least 20 contiguous adjacent pixels (up/down/left/right)."                                              |
| Output Requirements  | Files to generate (marked images, CSV data, reports) and formats       | "1. Mark voids in red in output images; 2. Export pixel grayscale data to `void_grayscale.csv`; 3. Generate a Word report with results." |

### Critical Notes


*   Refer to `MatImageAgent_Project/Mission_Descriptions/` for template MDs for TASK 1–3.

## 3. LLM API Interface and Account Information

MatImageAgent uses an API automation program (`MatImageAgent.py`) to interact with LLMs via their official APIs. The agent will send prompts (including the MD and conversation history) to the LLM and receive responses (e.g., Python code, debug suggestions).

### Supported LLMs

The agent has been validated with the following models (tested in our research):



*   GPT-4.1 (OpenAI)

*   Claude-3.7 (Anthropic)

*   DeepSeek-R1 (DeepSeek)


## 4. Running MatImageAgent

### 4.1 Pre-Install Dependencies

MatImageAgent relies on the following Python libraries. Install them via `pip` before running.


### 4.2 Execution Steps


1.  **Prepare Files**:

    Place the following files in the same working directory:

*   Core agent code: `MatImageAgent.py`

*   Your custom MD file: `[Your_Task]_MD.txt` (e.g., `SEM_Void_Analysis_MD.txt`)

*   Input images: Store in a subfolder (e.g., `./Input_Images/`) and specify the path in the MD.

1.  **Run the Agent**:

    Open the terminal, navigate to the working directory, and execute the following command:


```
python MatImageAgent.py -s \[Your\_Task]\_MD.txt > out.txt
```


*   `-s [Your_Task]_MD.txt`: Specifies the input MD file.

*   `> out.txt`: Logs the LLM conversation history, Python program outputs, and error messages to `out.txt` (for debugging).

### 4.3 Output Files

All generated files are saved in the working directory:



*   **Python Code**: Auto-generated scripts (e.g., `py1.py`) for image processing, verification and report generation.

*   **Processed Images**: Marked images (e.g., SEM voids in red, AFM phases in black/white).

*   **Data Files**: CSV files (e.g., `void_grayscale.csv`, `xct_grayscale_mapping.csv`) with quantitative results.

*   **Research Report**: A Word document (e.g., `SEM_Analysis_Report.docx`) with methods, results, and figures.

*   **Log File**: `out.txt` (debugging and execution history).

## 5. Repository Structure

This repo contains the following key files/folders:



```
MatImageAgent/
├── MatImageAgent_Project/
│   ├── Core_code/
│   │   └── MatImageAgent.py   # Core agent code (API automation + task execution)
│   ├── Demo/
│   └── Mission_Descriptions/  # Template MD files for TASK 1–3
│       ├── MD_T1.txt
│       ├── MD_T2.txt
│       └── MD_T3.txt
├── 10_Rycle_Rerun/            # TASK 1–3 rerun for 10 cycles for stability test
├── workflow.png               # A brif review of MatImageAgent
└── README.md                  # User guide (this file)
```
