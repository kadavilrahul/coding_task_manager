#!/bin/bash
set -e

# Install required tools
install_tools() {
    local tools=("cloc" "ripgrep:rg" "shellcheck" "jq" "tree")
    for tool in "${tools[@]}"; do
        local cmd="${tool#*:}"
        cmd="${cmd:-$tool}"
        if ! command -v "$cmd" &>/dev/null; then
            echo "Installing ${tool%:*}..."
            apt-get update -qq && apt-get install -y "${tool%:*}"
        fi
    done
}

# Check if command exists
cmd_exists() { command -v "$1" &>/dev/null; }

# Count lines of code
cloc_run() { cmd_exists cloc && cloc "${1:-.}" || echo "cloc not installed"; }

# Search for patterns
search() {
    local pattern="${1:-TODO}" path="${2:-.}"
    if cmd_exists rg; then
        rg "$pattern" "$path" -n --with-filename
    elif cmd_exists grep; then
        grep -rn "$pattern" "$path"
    else
        echo "No search tool available"
    fi
}

# Lint shell scripts
lint_sh() { cmd_exists shellcheck && find . -name "*.sh" -exec shellcheck {} + || echo "shellcheck not installed"; }

# Validate JSON files
lint_json() { cmd_exists jq && find . -name "*.json" -exec sh -c 'jq -e . "$1" >/dev/null && echo "✅ $1" || echo "❌ $1"' _ {} + || echo "jq not installed"; }

# Git statistics
git_stats() {
    [[ -d .git ]] || { echo "Not a git repository"; return; }
    echo "Commits: $(git rev-list --count HEAD 2>/dev/null || echo 'N/A')"
    echo "Contributors:"
    git shortlog -sn | head -5 2>/dev/null || echo "None"
}

# Show directory tree
tree_show() {
    local depth="${1:-2}"
    cmd_exists tree && tree -L "$depth" -I '.git|node_modules|__pycache__' || find . -maxdepth "$depth" -type d | head -20
}

# Generate comprehensive report
generate_report() {
    local path="${1:-.}"
    local report_file="reports/full_report_$(date +%Y%m%d_%H%M%S).md"
    mkdir -p reports
    
    {
        echo "# Project Analysis Report"
        echo "Generated: $(date)"
        echo "Project: $(basename "$(realpath "$path")")"
        echo "Path: $(realpath "$path")"
        echo -e "\n## Code Metrics"
        cloc_run "$path"
        echo -e "\n## Directory Structure\n\`\`\`"
        (cd "$path" && tree_show 3)
        echo -e "\`\`\`\n## Git Statistics"
        (cd "$path" && git_stats)
        echo -e "\n## File Summary"
        printf "- Shell scripts: %d\n" "$(find "$path" -name "*.sh" | wc -l)"
        printf "- JSON files: %d\n" "$(find "$path" -name "*.json" | wc -l)"
        printf "- Python files: %d\n" "$(find "$path" -name "*.py" | wc -l)"
    } | tee "$report_file"
    
    echo "Report generated: $report_file"
}

# Show menu
show_menu() {
    cat << 'EOF'

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

EOF
}

# Main interactive loop
main_loop() {
    while true; do
        show_menu
        read -rp "Enter your choice (0-7): " choice
        echo
        
        case $choice in
            1) read -rp "Path [.]: " path; cloc_run "${path:-.}" ;;
            2) read -rp "Pattern [TODO]: " pattern; read -rp "Path [.]: " path; search "${pattern:-TODO}" "${path:-.}" ;;
            3) lint_sh ;;
            4) lint_json ;;
            5) git_stats ;;
            6) read -rp "Depth [2]: " depth; tree_show "${depth:-2}" ;;
            7) read -rp "Path to analyze [.]: " path; generate_report "${path:-.}" ;;
            0) echo "Goodbye!"; exit 0 ;;
            *) echo "Invalid choice. Please enter 0-7." ;;
        esac
        
        echo
        read -rp "Press Enter to continue..."
    done
}

# Command line interface
if [[ $# -eq 0 ]]; then
    install_tools
    main_loop
else
    case "$1" in
        cloc) cloc_run "$2" ;;
        search) search "$2" "$3" ;;
        lint-sh) lint_sh ;;
        lint-json) lint_json ;;
        git-stats) git_stats ;;
        tree) tree_show "$2" ;;
        all) install_tools; generate_report "$2" ;;
        *) cat << 'EOF'
Usage: $0 {cloc|search|lint-sh|lint-json|git-stats|tree|all}

Commands:
  cloc [path]              - Count lines of code
  search [pattern] [path]  - Search for patterns
  lint-sh                  - Lint shell scripts
  lint-json                - Validate JSON files
  git-stats                - Show git statistics
  tree [depth]             - Show directory tree
  all [path]               - Run all and generate report

Run without arguments for interactive menu.
EOF
        ;;
    esac
fi
