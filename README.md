# PRD Generator

A Python-based tool that leverages the Gemini API to generate comprehensive Product Requirements Documents (PRDs) for new or existing software projects.

## Features

*   **AI-Powered PRD Generation**: Creates detailed PRDs using the Gemini model.
*   **Comprehensive PRD Sections**: Generates PRDs with sections like Executive Summary, Problem Statement, Functional Requirements, Technical Architecture, and more.
*   **Project Analysis**: Scans existing project files to analyze languages and frameworks, providing context for PRD generation.
*   **Flexible Project Types**: Supports PRD generation for both new projects and modifications to existing ones.
*   **Automated PRD Saving**: Automatically saves generated PRDs to a Markdown file with a timestamp.

## Prerequisites/System Requirements

*   **Operating System**: Tested on Linux.
*   **Python**: Python 3.8 or higher.
*   **pip**: Python package installer.
*   **Gemini API Key**: An active API key from Google Gemini.

## Installation

Follow these steps to set up and install the PRD Generator:

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

### 5. Verify Installation

After completing the steps above, you can verify your installation by running the main script. If it starts and prompts for input, the installation was successful.

```bash
python prd_generator.py
```

## Usage

To generate a PRD, run the `prd_generator.py` script from your terminal:

```bash
python prd_generator.py
```

The script will guide you through the following prompts:

1.  **Choose project type**:
    *   Enter `1` for a new project.
    *   Enter `2` for an existing project that needs modifications or enhancements. (If you choose 2, the tool will scan your current project files for context.)
2.  **Enter your product idea**: Provide a concise description of your product idea (e.g., "I want to simplify the project and use Gulp to generate html pages from csv files").

After you provide the product idea, the tool will generate a PRD and save it as a Markdown file (e.g., `PRD_product_DD-MM-YYYY_HHMMSS.md`) in the current directory.

## File Organization

*   [`prd_generator.py`](prd_generator.py): The main Python script for generating PRDs.
*   [`requirements.txt`](requirements.txt): Lists all Python dependencies required for the project.
*   [`INSTALLATION.md`](INSTALLATION.md): Provides detailed installation instructions.
*   [`PROMPT.md`](PROMPT.md): Defines the structure and style requirements for the `README.md` file.
*   [`.env`](.env): Configuration file for environment variables, specifically for the Gemini API key.
*   [`.gitignore`](.gitignore): Specifies intentionally untracked files to ignore by Git.
*   [`project_info.sh`](project_info.sh): A shell script that likely gathers project information.
*   [`project_info.txt`](project_info.txt): A text file that likely stores project information.

## Troubleshooting

*   **`ValueError: Missing GEMINI_API_KEY environment variable`**:
    *   **Solution**: Ensure you have created a `.env` file in the root directory and added your `GEMINI_API_KEY` as described in the "Configure Environment Variables" section. Double-check for typos in the key name or value.
*   **`ModuleNotFoundError`**:
    *   **Solution**: Make sure you have activated your virtual environment (`source venv/bin/activate` on Linux/macOS or `venv\Scripts\activate.bat` on Windows) and installed all dependencies using `pip install -r requirements.txt`.
*   **`agno` or `google-genai` related errors**:
    *   **Solution**: Verify that `pip install google-genai` was run successfully. Sometimes, specific versions might cause conflicts; ensure your `requirements.txt` is up-to-date or try reinstalling these specific packages.