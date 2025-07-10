# Coding Assistant Tools - Scripts 03

A minimalistic shell script that provides essential coding assistance utilities with both interactive menu and command-line interfaces, featuring optional report generation.

## Features

### 📊 Code Analysis & Metrics
- **CLOC** - Count lines of code, comments, and blank lines by language

### 🔍 Code Search & Navigation  
- **Pattern Search** - Fast text search using RipGrep or grep fallback

### 🏗️ Code Structure Analysis
- **Directory Tree** - Display project structure with customizable depth

### ✅ Code Quality & Linting
- **ShellCheck** - Find bugs and issues in shell scripts
- **JSON Validation** - Validate JSON files using jq

### 📈 Git & Version Control
- **Git Statistics** - Repository metrics including commits and contributors

### 📋 Report Generation
- **Individual Reports** - Save any command output as timestamped reports
- **Comprehensive Reports** - Generate full project analysis in Markdown format

## Usage

### Interactive Mode
```bash
./coding_assistant_tools.sh
```

The script provides a numbered menu interface:
```
Coding Assistant Tools
======================
1) Count lines of code
2) Search for patterns
3) Lint shell scripts
4) Validate JSON files
5) Show git statistics
6) Show directory tree
7) Generate full report
0) Exit
```

After each command execution, you'll be prompted to save the results as a report.

### Command Line Mode
```bash
./coding_assistant_tools.sh {command} [options]
```

Available commands:
- `cloc [path]` - Count lines of code
- `search [pattern] [path]` - Search for patterns
- `lint-sh` - Lint shell scripts
- `lint-json` - Validate JSON files
- `git-stats` - Show git statistics
- `tree [depth]` - Show directory tree
- `report` - Generate full project report

## Installation

The script gracefully handles missing tools by checking for their availability and providing informative messages. No automatic installation is performed - you can install tools manually as needed.

## Supported Platforms

- Linux (all distributions)
- macOS (with compatible tools)
- Windows (with WSL or compatible shell)

## Dependencies

Optional tools that enhance functionality:
- `cloc` - For code metrics
- `ripgrep` (rg) - For fast pattern searching (falls back to grep)
- `tree` - For directory visualization (falls back to find)
- `shellcheck` - For shell script linting
- `jq` - For JSON validation
- `git` - For repository statistics

## Report Generation

The script can generate timestamped reports in the `reports/` directory:

### Individual Command Reports
- `cloc_analysis_YYYYMMDD_HHMMSS.txt` - Code metrics analysis
- `search_results_YYYYMMDD_HHMMSS.txt` - Pattern search results
- `shellcheck_report_YYYYMMDD_HHMMSS.txt` - Shell script linting results
- `json_validation_YYYYMMDD_HHMMSS.txt` - JSON validation results
- `git_statistics_YYYYMMDD_HHMMSS.txt` - Git repository statistics
- `directory_tree_YYYYMMDD_HHMMSS.txt` - Directory structure visualization

### Comprehensive Report
- `full_report_YYYYMMDD_HHMMSS.md` - Complete project analysis in Markdown format

Reports are generated with timestamps to avoid conflicts and provide historical tracking.

## Examples

### Interactive Mode Examples

#### Code Analysis with Report Saving
```bash
./coding_assistant_tools.sh
# Choose option 1 (Count lines of code)
# Enter path or press Enter for current directory
# Choose 'y' when prompted to save as report
```

#### Pattern Search
```bash
./coding_assistant_tools.sh
# Choose option 2 (Search for patterns)
# Enter search pattern (e.g., "TODO", "FIXME", "function")
# Enter path or press Enter for current directory
# Choose 'y' to save results as report
```

#### Generate Full Project Report
```bash
./coding_assistant_tools.sh
# Choose option 7 (Generate full report)
# Report automatically saved as Markdown file
```

### Command Line Examples

#### Direct Commands
```bash
# Count lines of code in current directory
./coding_assistant_tools.sh cloc

# Search for TODO comments
./coding_assistant_tools.sh search "TODO"

# Lint all shell scripts
./coding_assistant_tools.sh lint-sh

# Generate comprehensive report
./coding_assistant_tools.sh report

# Show directory tree with depth 3
./coding_assistant_tools.sh tree 3
```

## Key Features

- **Minimalistic Design** - Clean, focused functionality without bloat
- **Dual Interface** - Both interactive menu and command-line modes
- **Graceful Degradation** - Falls back to basic tools when advanced ones aren't available
- **Optional Report Generation** - Save any output as timestamped reports
- **Cross-Platform** - Works on Linux, macOS, and Windows (with compatible shell)
- **No Dependencies** - Core functionality works with standard Unix tools
- **User-Friendly** - Clear numbered menus and helpful prompts

## Sample Report Output

The comprehensive report includes:
```markdown
# Project Analysis Report
Generated: [timestamp]
Project: [project-name]

## Code Metrics
[CLOC analysis with language breakdown]

## Directory Structure
[Tree visualization of project structure]

## Git Statistics
[Repository metrics and contributor information]

## File Summary
[Count of different file types]
```

## Contributing

To extend functionality:
1. Add new functions following the existing pattern
2. Update the menu system in `show_menu()` and `main_loop()`
3. Add command-line support in the case statement
4. Update this README with new features
5. Test both interactive and command-line modes

## License

MIT License - Feel free to use and modify as needed.