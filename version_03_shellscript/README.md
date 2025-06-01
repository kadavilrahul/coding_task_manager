# Agno Code Tools - Shell Script Version

This project provides a comprehensive set of shell scripts to help with code analysis and modification using the Gemini API. The scripts are designed to be robust, secure, and user-friendly with extensive error handling and validation.

## Features

### Core Scripts

- **`project_info.sh`**: Comprehensive project analysis including file structure, sensitive information scanning, and code metrics
- **`generate_prd.sh`**: AI-powered Product Requirements Document generation using Gemini API
- **`file_paths.sh`**: Advanced file search with filtering, pattern matching, and interactive mode
- **`extract_functions.sh`**: Multi-language function extraction with support for Python, JavaScript, and Bash
- **`modify_code.sh`**: AI-assisted code modification with backup, dry-run, and validation features
- **`identify_changes.sh`**: Advanced file comparison with multiple output formats (diff, HTML, JSON)
- **`join_code.sh`**: Intelligent code file merging with formatting and organization options

### Key Improvements

✅ **Security Enhancements:**
- Proper JSON escaping to prevent injection attacks
- Secure API key handling
- Input validation and sanitization

✅ **Error Handling:**
- Comprehensive error checking with `set -e`
- Graceful failure handling
- Informative error messages

✅ **User Experience:**
- Interactive and command-line modes
- Comprehensive help documentation
- Progress indicators and status messages

✅ **Robustness:**
- Automatic cleanup of temporary files
- File existence validation
- Dependency checking

✅ **Flexibility:**
- Multiple output formats
- Configurable options
- Language auto-detection

## Quick Start

1. **Install dependencies:**
   ```bash
   sudo apt update && sudo apt install git jq curl tree  # Ubuntu/Debian
   ```

2. **Set up Gemini API key:**
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

3. **Make scripts executable:**
   ```bash
   chmod +x *.sh
   ```

4. **Analyze your project:**
   ```bash
   ./project_info.sh
   ./generate_prd.sh
   ```

## Script Details

### project_info.sh
Gathers comprehensive project information including:
- File structure (using `tree` or `find` fallback)
- Sensitive information scanning (API keys, secrets, etc.)
- Code metrics for multiple file types
- User-provided project description

**Features:**
- Automatic cleanup of temporary files
- Enhanced sensitive pattern detection
- Support for multiple programming languages
- Timestamped output

### generate_prd.sh
Generates Product Requirements Documents using Gemini AI:
- Secure JSON payload construction
- Comprehensive error handling
- Formatted output with timestamps
- Raw response preservation for debugging

**Features:**
- JSON injection prevention
- API error handling
- Response validation
- Multiple output formats

### file_paths.sh
Advanced file search and discovery:
- Interactive and command-line modes
- Pattern matching with regex support
- File type filtering
- Case-insensitive search options

**Usage Examples:**
```bash
./file_paths.sh                    # Interactive mode
./file_paths.sh main.py            # Search for "main.py"
./file_paths.sh -t py main         # Python files containing "main"
./file_paths.sh -i README          # Case-insensitive search
```

### extract_functions.sh
Multi-language function extraction:
- Support for Python, JavaScript, and Bash
- Separate or combined output modes
- Language auto-detection
- Proper function boundary detection

**Usage Examples:**
```bash
./extract_functions.sh main.py                    # Extract Python functions
./extract_functions.sh -l javascript script.js   # Extract JS functions
./extract_functions.sh -f single utils.py        # Single output file
```

### modify_code.sh
AI-powered code modification:
- Function-specific or file-wide modifications
- Backup creation before changes
- Dry-run mode for preview
- Custom modification prompts

**Usage Examples:**
```bash
./modify_code.sh main.py calculate_sum           # Modify specific function
./modify_code.sh -p "Add error handling" utils.py # Custom prompt
./modify_code.sh -b -d script.py                 # Backup + dry-run
```

### identify_changes.sh
Advanced file comparison:
- Multiple diff formats (unified, side-by-side)
- HTML and JSON output options
- Change statistics
- Configurable context lines

**Usage Examples:**
```bash
./identify_changes.sh old.py new.py              # Basic diff
./identify_changes.sh -s file1.txt file2.txt     # Side-by-side
./identify_changes.sh -f html --stats f1 f2      # HTML with stats
```

### join_code.sh
Intelligent code file merging:
- Directory-based file collection
- Pattern matching and exclusion
- Auto-formatting support
- File organization with comments

**Usage Examples:**
```bash
./join_code.sh combined.py file1.py file2.py     # Basic join
./join_code.sh -c -n all.js src/*.js             # With comments/numbers
./join_code.sh -d -p '*.py' combined.py src/     # Directory-based
```

## Dependencies

**Required:**
- `bash` (4.0+)
- `jq` (JSON processing)
- `curl` (API calls)
- `grep`, `awk`, `sed` (text processing)

**Optional (for enhanced functionality):**
- `tree` (better directory listing)
- `black`, `autopep8` (Python formatting)
- `prettier` (JavaScript formatting)
- `gofmt` (Go formatting)

## Security Considerations

- API keys are handled securely without logging
- Input validation prevents injection attacks
- Temporary files are automatically cleaned up
- Sensitive information scanning helps identify security issues

## Error Handling

All scripts include comprehensive error handling:
- Input validation
- Dependency checking
- API error handling
- Graceful failure recovery
- Informative error messages

## Contributing

The scripts are designed to be modular and extensible. To add support for new languages or features:

1. Follow the existing error handling patterns
2. Add comprehensive input validation
3. Include usage documentation
4. Test with various edge cases

## License

This project is provided as-is for educational and development purposes. Please review and test thoroughly before using in production environments.