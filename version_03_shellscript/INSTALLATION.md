# Installation Guide

This guide provides commands to install and run the Agno Code Tools.

## Prerequisites

1.  **Install Required System Tools:**

    **Debian/Ubuntu:**
    ```bash
    sudo apt update && sudo apt install git jq curl tree
    ```
    
    **Fedora/CentOS/RHEL:**
    ```bash
    sudo dnf install git jq curl tree
    ```
    
    **macOS (using Homebrew):**
    ```bash
    brew install git jq curl tree
    ```

2.  **Set up the Gemini API key:**

    *   Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
    *   Set the `GEMINI_API_KEY` environment variable:
        
        ```bash
        export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        ```
        
        To make it permanent, add it to your shell profile:
        ```bash
        echo 'export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"' >> ~/.bashrc
        source ~/.bashrc
        ```
        
        You can verify the setup by running:
        ```bash
        echo $GEMINI_API_KEY
        ```

## Installation

3.  **Download the code:**

    ```bash
    git clone <repository_url>
    cd agno-code-tools/version_03_shellscript
    ```

    (Replace `<repository_url>` with the URL of this repository)

4.  **Make the scripts executable:**

    ```bash
    chmod +x *.sh
    ```

## Usage

5.  **Run the project info script:**

    ```bash
    ./project_info.sh
    ```

    This will:
    - Scan your project structure
    - Look for sensitive information
    - Count lines of code
    - Prompt you for a project description
    - Generate `project_info.txt`

6.  **Generate a PRD using Gemini:**

    ```bash
    ./generate_prd.sh
    ```

    This will:
    - Read the project information
    - Send it to Gemini API for analysis
    - Generate a Product Requirements Document
    - Save results to `gemini_prd.txt`

7.  **Use other scripts as needed:**

    **Search for files:**
    ```bash
    ./file_paths.sh                    # Interactive mode
    ./file_paths.sh main.py            # Search for files containing "main.py"
    ./file_paths.sh -t py main         # Search Python files containing "main"
    ./file_paths.sh -i README          # Case-insensitive search
    ```

    **Extract functions from code:**
    ```bash
    ./extract_functions.sh main.py                    # Extract from Python file
    ./extract_functions.sh -l javascript script.js   # Extract from JavaScript
    ./extract_functions.sh -o functions src/utils.py # Custom output directory
    ```

    **Modify code with AI:**
    ```bash
    ./modify_code.sh main.py calculate_sum           # Modify specific function
    ./modify_code.sh -p "Add error handling" utils.py # Custom prompt
    ./modify_code.sh -b -d script.py                 # Backup and dry-run
    ```

    **Compare files:**
    ```bash
    ./identify_changes.sh old_file.py new_file.py    # Basic diff
    ./identify_changes.sh -s file1.txt file2.txt     # Side-by-side view
    ./identify_changes.sh --stats -o diff.txt f1 f2  # With statistics
    ./identify_changes.sh -f html file1 file2        # HTML output
    ```

    **Join multiple files:**
    ```bash
    ./join_code.sh combined.py file1.py file2.py file3.py  # Basic join
    ./join_code.sh -c -n all_scripts.js src/*.js           # With comments and line numbers
    ./join_code.sh -d -p '*.py' combined.py src/           # Join all Python files from directory
    ```

## Optional Enhancements

For better functionality, you can install additional tools:

**Code Formatters:**
```bash
# Python
pip install black autopep8

# JavaScript/TypeScript
npm install -g prettier

# Go
# gofmt is included with Go installation

# Java
# Download google-java-format from GitHub releases

# Rust
# rustfmt is included with Rust installation
```

## Troubleshooting

**Common Issues:**

1. **"jq: command not found"**
   - Install jq using your package manager (see Prerequisites)

2. **"tree: command not found"**
   - Install tree using your package manager, or the script will use `find` as fallback

3. **"API Error: Invalid API key"**
   - Verify your Gemini API key is correctly set
   - Check that the key has proper permissions

4. **"Permission denied" when running scripts**
   - Make sure scripts are executable: `chmod +x *.sh`

5. **Empty or malformed API responses**
   - Check your internet connection
   - Verify the API key is valid and has quota remaining
   - Check the raw response files for debugging information

## Security Notes

- Never commit your API key to version control
- The scripts create temporary files that are cleaned up automatically
- Sensitive information scanning helps identify potential security issues
- Always review AI-generated code modifications before applying them to production