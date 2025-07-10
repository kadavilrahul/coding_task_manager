# Coding Assistant - Version 02

This directory contains scripts and configuration files for a coding assistant.

## Files

*   `sop.json`: Standard Operating Procedure for the coding assistant. This file defines the AI persona, guidelines, and example prompts for the assistant.
*   `run_cloc.sh`: Script to analyze the project's code using `cloc`.
*   `collect_functions.sh`: Script to collect function names from the codebase using `grep` or `ctags`.
*   `extract_functions.py`: Python script to extract function names from Python files using the `ast` module.

## Usage

1.  Modify `sop.json` to customize the coding assistant's behavior.
2.  Run `run_cloc.sh` to analyze the project's code.
3.  Run `collect_functions.sh` to collect function names from the codebase.

**Set up Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    ```
**Run script**:
    ```bash
    python extract_functions.py
    ```

## Dependencies

*   `cloc` (for `run_cloc.sh`)
*   `ctags` (for `collect_functions.sh`)
*   Python 3 (for `extract_functions.py`)

## License

[Your License]