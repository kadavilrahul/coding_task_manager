# AI-Powered Scripting Tools

This project provides a suite of AI-powered scripting tools for automating various development tasks, including PRD generation, code generation, and MCP integration.

1.  **Set up Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    pip install google-genai
    ```
3.  **Configure API Key**: Create a `.env` file in the root directory with your Gemini API key:
    ```
    GEMINI_API_KEY='your_gemini_api_key_here'
    ```
4.  **Generate Project Information**: Run:
    ```bash
    bash 00_generate_project_info.sh
    ```
5.  **Generate a Product Requirements Document (PRD)**: Run:
    ```bash
    python 00_generate_prd.py
    ```
6.  **AI-Assisted Code Development**: This is designed to work with AI code editor extensions using [`00_generate_code_using_sop.json`](00_generate_code_using_sop.json) and [`00_generate_run_script.json`](00_generate_run_script.json).
7.  **MCP Integration for GitHub Copilot**: Follow the instructions in [`00_generate_mcp.md`](00_generate_mcp.md) to set up and test Hugging Face MCP integration with GitHub Copilot.

## Features

*   **AI-Powered PRD Generation**: Creates detailed Product Requirements Documents (PRDs) using the Gemini model.
*   **Standard Operating Procedure (SOP) for AI Development**: Provides a comprehensive JSON-based SOP (`00_generate_code_using_sop.json`) to guide AI behavior in code generation, review, testing, and documentation within VS Code.
*   **Prompt for Run Script Generation**: Includes a JSON prompt (`00_generate_run_script.json`) to guide AI in generating `run.sh` scripts.
*   **Project Information Generation**: Gathers and summarizes project structure, sensitive information, and line counts.
*   **Workflow with AI Code Editor Extensions**: Designed for seamless integration with AI code editor extensions in VS Code, leveraging PRDs and SOPs for contextual awareness and task execution.
*   **MCP Integration for GitHub Copilot**: Provides instructions for setting up and testing Hugging Face MCP integration specifically for GitHub Copilot (Agent mode).

## File Organization

*   [`00_generate_prd.py`](00_generate_prd.py): Main Python script for generating PRDs.
*   [`requirements.txt`](requirements.txt): Python dependencies.
*   [`00_generate_code_using_sop.json`](00_generate_code_using_sop.json): AI's SOP for development.
*   [`00_generate_run_script.json`](00_generate_run_script.json): Prompt for `run.sh` script generation.
*   [`.env`](.env): Environment variables (Gemini API key).
*   [`00_generate_project_info.sh`](00_generate_project_info.sh): Script to gather project information.
*   [`00_generate_mcp.md`](00_generate_mcp.md): Instructions for MCP setup and testing with GitHub Copilot.

## Troubleshooting

*   **`ValueError: Missing GEMINI_API_KEY environment variable`**: Ensure `.env` file is created with `GEMINI_API_KEY`.
*   **`ModuleNotFoundError`**: Activate virtual environment and install dependencies (`pip install -r requirements.txt`).
*   **`google-genai` related errors**: Verify `pip install google-genai` was successful.
