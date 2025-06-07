# Coding Task Manager

A Python-based tool that leverages the Gemini API to generate Product Requirements Documents (PRDs) and provides a structured Standard Operating Procedure (SOP) for AI-assisted software development within VS Code. It also includes tools for generating project information and run scripts.

## Features

*   **AI-Powered PRD Generation**: Creates detailed Product Requirements Documents (PRDs) using the Gemini model, with sections like Executive Summary, Problem Statement, Functional Requirements, and Technical Architecture. It can analyze existing project files for context.
*   **Standard Operating Procedure (SOP) for AI Development**: Provides a comprehensive JSON-based SOP (`ai_development_sop.json`) to guide AI behavior in code generation, review, testing, and documentation within VS Code, designed for automated use by AI code editor extensions.
*   **Prompt for Run Script Generation**: Includes a JSON prompt (`generate_run_script.json`) to guide AI in generating `run.sh` scripts for various codebases, automating environment setup and execution.
*   **Project Information Generation**: Gathers and summarizes project structure, sensitive information, and line counts.

## Prerequisites/System Requirements

*   **Operating System**: Tested on Linux.
*   **Python**: Python 3.8 or higher.
*   **pip**: Python package installer.
*   **Gemini API Key**: An active API key from Google Gemini.

## Installation

Follow these steps to set up and install the tools:

### Clone the Script
Clone the repository or download the script manually:
```
git clone https://github.com/kadavilrahul/coding_task_manager.git
```
```
cd coding_task_manager
```

### 1. Create Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create virtual environment
python3 -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows (Command Prompt):
# venv\Scripts\activate.bat

# On Windows (PowerShell):
# venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory of the project and add your Gemini API key.

```
GEMINI_API_KEY='your_gemini_api_key_here'
```

Replace `'your_gemini_api_key_here'` with your actual Gemini API key.

### 4. Install google-genai library

This library is specifically required for `agno` to interact with the Gemini API.

```bash
pip install google-genai
```

## Usage

This repository provides tools and documentation to facilitate AI-assisted software development.

### 1. Generate Project Information

To gather project information (structure, line counts, etc.), run the `project_info.sh` script:

```bash
bash project_info.sh
```

### 2. Generate a Product Requirements Document (PRD)

To create a PRD for a new or existing project, run the `generate_prd.py` script:

```bash
python generate_prd.py
```
The script will prompt you to choose a project type (new or existing) and enter your product idea. It will then generate a PRD and save it as a Markdown file (e.g., `PRD_product_DD-MM-YYYY_HHMMSS.md`) in the current directory.

### 3. AI-Assisted Code Development

This project is designed to work seamlessly with AI code editor extensions in VS Code. The AI's behavior and operational guidelines are defined in `ai_development_sop.json`.

*   **`ai_development_sop.json`**: This JSON file contains the comprehensive Standard Operating Procedure for the AI. It defines the AI's persona, prompt templates for various tasks (code generation, review, testing, debugging, documentation), and operational guidelines. AI code editor extensions should use this file to guide the AI's actions without requiring direct user input for prompt construction.
    *   **Key References**: This SOP refers to the generated PRD (e.g., `PRD_[timestamp].md`), `project_info.txt`, and files within the `/reference` folder for context.

*   **`generate_run_script.json`**: This JSON file provides a prompt template specifically for generating `run.sh` scripts. AI code editor extensions can use this to instruct the AI to create executable shell scripts for setting up environments, installing dependencies, and running codebases.

**Workflow with AI Code Editor Extensions:**

1.  **PRD Generation**: Use `generate_prd.py` to create your project's PRD.
2.  **AI Guidance**: The AI code editor extension will automatically leverage `ai_development_sop.json` to understand its role and how to interact with the project.
3.  **Task Execution**: Based on your high-level instructions within the editor, the extension will construct detailed prompts (using templates from `ai_development_sop.json`) and send them to the AI for tasks like:
    *   Generating new code.
    *   Reviewing existing code.
    *   Refining code.
    *   Generating unit tests.
    *   Assisting with debugging.
    *   Generating documentation.
    *   Generating `run.sh` scripts (using `generate_run_script.json`).
4.  **Contextual Awareness**: The AI will automatically refer to the generated PRD, `project_info.txt`, and the `reference/` folder for necessary project context, ensuring relevant and accurate outputs.

## File Organization

*   [`generate_prd.py`](generate_prd.py): The main Python script for generating PRDs.
*   [`requirements.txt`](requirements.txt): Lists all Python dependencies required for the project.
*   [`generate_readme.md`](generate_readme.md): Defines the structure and style requirements for the `README.md` file.
*   [`ai_development_sop.json`](ai_development_sop.json): A comprehensive JSON file defining the AI's persona, prompt templates, and operational guidelines for AI-assisted software development.
*   [`generate_run_script.json`](generate_run_script.json): A JSON prompt template for guiding AI in generating `run.sh` scripts for various codebases.
*   [`.env`](.env): Configuration file for environment variables, specifically for the Gemini API key.
*   [`.gitignore`](.gitignore): Specifies intentionally untracked files to ignore by Git.
*   [`project_info.sh`](project_info.sh): A shell script that gathers project information.


## Troubleshooting

*   **`ValueError: Missing GEMINI_API_KEY environment variable`**:
    *   **Solution**: Ensure you have created a `.env` file in the root directory and added your `GEMINI_API_KEY` as described in the "Configure Environment Variables" section. Double-check for typos in the key name or value.
*   **`ModuleNotFoundError`**:
    *   **Solution**: Make sure you have activated your virtual environment (`source venv/bin/activate` on Linux/macOS or `venv\Scripts\activate.bat` on Windows) and installed all dependencies using `pip install -r requirements.txt`.
*   **`agno` or `google-genai` related errors**:
    *   **Solution**: Verify that `pip install google-genai` was run successfully. Sometimes, specific versions might cause conflicts; ensure your `requirements.txt` is up-to-date or try reinstalling these specific packages.
