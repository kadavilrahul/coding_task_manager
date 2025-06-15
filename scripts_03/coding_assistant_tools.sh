#!/bin/bash
set -e

# Simple coding assistant tools

# Check if command exists
cmd_exists() { command -v "$1" >/dev/null 2>&1; }

# Count lines of code
cloc_run() {
    if cmd_exists cloc; then
        cloc "${1:-.}"
    else
        echo "cloc not installed"
    fi
}

# Search for patterns
search() {
    local pattern="${1:-TODO}"
    local path="${2:-.}"
    if cmd_exists rg; then
        rg "$pattern" "$path" --line-number --with-filename
    elif cmd_exists grep; then
        grep -rn "$pattern" "$path"
    else
        echo "No search tool available"
    fi
}

# Lint shell scripts
lint_sh() {
    if cmd_exists shellcheck; then
        find . -name "*.sh" -exec shellcheck {} \;
    else
        echo "shellcheck not installed"
    fi
}

# Validate JSON files
lint_json() {
    if cmd_exists jq; then
        find . -name "*.json" -exec sh -c 'jq empty "$1" && echo "✅ $1" || echo "❌ $1"' _ {} \;
    else
        echo "jq not installed"
    fi
}

# Git statistics
git_stats() {
    if [[ -d .git ]]; then
        echo "Commits: $(git rev-list --count HEAD 2>/dev/null || echo 'N/A')"
        echo "Contributors:"
        git shortlog -sn | head -5 2>/dev/null || echo "None"
    else
        echo "Not a git repository"
    fi
}

# Show directory tree
tree_show() {
    local depth="${1:-2}"
    if cmd_exists tree; then
        tree -L "$depth" -I '.git|node_modules|__pycache__'
    else
        find . -maxdepth "$depth" -type d | head -20
    fi
}

# Create reports directory if it doesn't exist
ensure_reports_dir() { [[ ! -d "reports" ]] && mkdir -p reports; }

# Generate timestamp for report filenames
timestamp() { date +"%Y%m%d_%H%M%S"; }

# Save output to report file
save_to_report() {
    local content="$1"
    local report_type="$2"
    ensure_reports_dir
    local report_file="reports/${report_type}_$(timestamp).txt"
    echo "$content" > "$report_file"
    echo "Report saved: $report_file"
}

# Show menu
show_menu() {
    echo ""
    echo "Coding Assistant Tools"
    echo "======================"
    echo "1) Count lines of code"
    echo "2) Search for patterns"
    echo "3) Lint shell scripts"
    echo "4) Validate JSON files"
    echo "5) Show git statistics"
    echo "6) Show directory tree"
    echo "7) Generate full report"
    echo "0) Exit"
    echo ""
}

# Generate comprehensive report
generate_report() {
    ensure_reports_dir
    local report_file="reports/full_report_$(timestamp).md"
    
    echo "Generating comprehensive report..."
    {
        echo "# Project Analysis Report"
        echo "Generated: $(date)"
        echo "Project: $(basename "$(pwd)")"
        echo ""
        
        echo "## Code Metrics"
        if cmd_exists cloc; then
            cloc . --md 2>/dev/null || echo "Code metrics unavailable"
        else
            echo "cloc not installed"
        fi
        echo ""
        
        echo "## Directory Structure"
        echo "\`\`\`"
        if cmd_exists tree; then
            tree -L 3 -I '.git|node_modules|__pycache__' 2>/dev/null || echo "Tree unavailable"
        else
            find . -maxdepth 3 -type d | head -20
        fi
        echo "\`\`\`"
        echo ""
        
        echo "## Git Statistics"
        if [[ -d .git ]]; then
            echo "- Commits: $(git rev-list --count HEAD 2>/dev/null || echo 'N/A')"
            echo "- Contributors: $(git shortlog -sn | wc -l 2>/dev/null || echo 'N/A')"
            echo "- Last commit: $(git log -1 --format=%cd 2>/dev/null || echo 'N/A')"
        else
            echo "Not a git repository"
        fi
        echo ""
        
        echo "## File Summary"
        local shell_count=$(find . -name "*.sh" 2>/dev/null | wc -l)
        local json_count=$(find . -name "*.json" 2>/dev/null | wc -l)
        local py_count=$(find . -name "*.py" 2>/dev/null | wc -l)
        echo "- Shell scripts: $shell_count"
        echo "- JSON files: $json_count"
        echo "- Python files: $py_count"
        
    } > "$report_file"
    
    echo "Full report generated: $report_file"
}

# Main interactive loop
main_loop() {
    while true; do
        show_menu
        read -p "Enter your choice (0-7): " choice
        echo ""
        
        case $choice in
            1)
                read -p "Enter path to analyze [current directory]: " path
                output=$(cloc_run "${path:-.}" 2>&1)
                echo "$output"
                read -p "Save as report? (y/N): " save
                if [[ "$save" =~ ^[Yy]$ ]]; then
                    save_to_report "$output" "cloc_analysis"
                fi
                ;;
            2)
                read -p "Enter search pattern [TODO]: " pattern
                read -p "Enter path to search [current directory]: " path
                output=$(search "${pattern:-TODO}" "${path:-.}" 2>&1)
                echo "$output"
                read -p "Save as report? (y/N): " save
                if [[ "$save" =~ ^[Yy]$ ]]; then
                    save_to_report "$output" "search_results"
                fi
                ;;
            3)
                output=$(lint_sh 2>&1)
                echo "$output"
                read -p "Save as report? (y/N): " save
                if [[ "$save" =~ ^[Yy]$ ]]; then
                    save_to_report "$output" "shellcheck_report"
                fi
                ;;
            4)
                output=$(lint_json 2>&1)
                echo "$output"
                read -p "Save as report? (y/N): " save
                if [[ "$save" =~ ^[Yy]$ ]]; then
                    save_to_report "$output" "json_validation"
                fi
                ;;
            5)
                output=$(git_stats 2>&1)
                echo "$output"
                read -p "Save as report? (y/N): " save
                if [[ "$save" =~ ^[Yy]$ ]]; then
                    save_to_report "$output" "git_statistics"
                fi
                ;;
            6)
                read -p "Enter tree depth [2]: " depth
                output=$(tree_show "${depth:-2}" 2>&1)
                echo "$output"
                read -p "Save as report? (y/N): " save
                if [[ "$save" =~ ^[Yy]$ ]]; then
                    save_to_report "$output" "directory_tree"
                fi
                ;;
            7)
                generate_report
                ;;
            0)
                echo "Goodbye!"
                exit 0
                ;;
            *)
                echo "Invalid choice. Please enter a number between 0-7."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Command line mode or interactive mode
if [[ $# -eq 0 ]]; then
    main_loop
else
    case "$1" in
        cloc) cloc_run "$2" ;;
        search) search "$2" "$3" ;;
        lint-sh) lint_sh ;;
        lint-json) lint_json ;;
        git-stats) git_stats ;;
        tree) tree_show "$2" ;;
        report)
            generate_report
            ;;
        *)
            echo "Usage: $0 {cloc|search|lint-sh|lint-json|git-stats|tree|report}"
            echo ""
            echo "Commands:"
            echo "  cloc [path]           - Count lines of code"
            echo "  search [pattern] [path] - Search for patterns"
            echo "  lint-sh               - Lint shell scripts"
            echo "  lint-json             - Validate JSON files"
            echo "  git-stats             - Show git statistics"
            echo "  tree [depth]          - Show directory tree"
            echo "  report                - Generate full project report"
            echo ""
            echo "Or run without arguments for interactive menu."
            ;;
    esac
fi