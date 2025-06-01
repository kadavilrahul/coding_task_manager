# Agno Code Tools

This project provides a set of shell scripts to help with code analysis and modification using the Gemini API.

## Scripts

- `project_info.sh`: Gathers project information, including file structure, sensitive information (API keys, database URLs), and line counts.
- `generate_prd.sh`: Generates a PRD (Product Requirements Document) and prompt for Gemini, based on the project information.
- `file_paths.sh`: Lists project file paths, allowing you to search for specific files.
- `extract_functions.sh`: Extracts function definitions from code files.
- `modify_code.sh`: Modifies code using the Gemini API.
- `identify_changes.sh`: Identifies changes between two files using `diff`.
- `join_code.sh`: Joins multiple code files into a single file.

## Usage

1.  Run `project_info.sh` to generate `project_info.txt`.
2.  Use the other scripts as needed to analyze and modify your code.

## Notes

- The `extract_functions.sh` and `modify_code.sh` scripts require more sophisticated parsing and code modification techniques for robust functionality. Consider using `tree-sitter` CLI or language-specific refactoring libraries for better results.
- These scripts are provided as a starting point and may need to be adapted to your specific project and needs.