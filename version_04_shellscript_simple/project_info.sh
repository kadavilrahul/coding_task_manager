#!/bin/bash

set -e  # Exit on any error

# Function to cleanup temporary files
cleanup() {
    rm -f project_structure.txt sensitive_info.txt line_counts.txt
}

# Set trap to cleanup on exit
trap cleanup EXIT

echo "Gathering project information..."

# Check if an argument is provided
if [ -z "$1" ]; then
    directory="."
else
    directory="$1"
fi

# Function to generate tree structure
generate_tree() {
    local dir="$1"
    local prefix="$2"
    local is_last="$3"
    
    # Skip if directory doesn't exist or is excluded
    if [ ! -d "$dir" ]; then
        return
    fi
    
    # Get list of items, excluding unnecessary files and directories
    local items=()
    while IFS= read -r -d '' item; do
        local basename=$(basename "$item")
        # Skip hidden files and unnecessary files/directories
        if [[ ! "$basename" =~ ^\. ]] && \
           [[ "$basename" != "node_modules" ]] && \
           [[ "$basename" != "__pycache__" ]] && \
           [[ "$basename" != "venv" ]] && \
           [[ "$basename" != "env" ]] && \
           [[ "$basename" != ".venv" ]] && \
           [[ "$basename" != "dist" ]] && \
           [[ "$basename" != "build" ]] && \
           [[ "$basename" != "target" ]] && \
           [[ "$basename" != "bin" ]] && \
           [[ "$basename" != "obj" ]] && \
           [[ "$basename" != ".next" ]] && \
           [[ "$basename" != ".nuxt" ]] && \
           [[ "$basename" != "coverage" ]] && \
           [[ "$basename" != ".pytest_cache" ]] && \
           [[ "$basename" != ".mypy_cache" ]] && \
           [[ "$basename" != "*.log" ]] && \
           [[ "$basename" != "*.tmp" ]] && \
           [[ "$basename" != "*.cache" ]] && \
           [[ ! "$basename" =~ \.env$ ]] && \
           [[ ! "$basename" =~ \.env\. ]] && \
           [[ ! "$basename" =~ \.pyc$ ]] && \
           [[ ! "$basename" =~ \.pyo$ ]] && \
           [[ ! "$basename" =~ \.class$ ]] && \
           [[ ! "$basename" =~ \.o$ ]] && \
           [[ ! "$basename" =~ \.so$ ]] && \
           [[ ! "$basename" =~ \.dll$ ]] && \
           [[ ! "$basename" =~ \.exe$ ]] && \
           [[ ! "$basename" =~ \.DS_Store$ ]] && \
           [[ ! "$basename" =~ Thumbs\.db$ ]]; then
            items+=("$item")
        fi
    done < <(find "$dir" -maxdepth 1 -mindepth 1 -print0 | sort -z)
    
    local count=${#items[@]}
    local i=0
    
    for item in "${items[@]}"; do
        i=$((i + 1))
        local is_last_item=false
        if [ $i -eq $count ]; then
            is_last_item=true
        fi
        
        local basename=$(basename "$item")
        
        if [ -d "$item" ]; then
            if $is_last_item; then
                echo "${prefix}└── $basename/"
                generate_tree "$item" "${prefix}    " true
            else
                echo "${prefix}├── $basename/"
                generate_tree "$item" "${prefix}│   " false
            fi
        else
            if $is_last_item; then
                echo "${prefix}└── $basename"
            else
                echo "${prefix}├── $basename"
            fi
        fi
    done
}

# Generate project structure
echo "Generating project structure..."
{
    echo "=== Project Structure ==="
    if command -v tree >/dev/null 2>&1; then
        # Use tree if available with comprehensive exclusions
        tree "$directory" -a -I '.git|.svn|.hg|node_modules|__pycache__|venv|env|.venv|dist|build|target|bin|obj|.next|.nuxt|coverage|.pytest_cache|.mypy_cache|*.pyc|*.pyo|*.class|*.o|*.so|*.dll|*.exe|*.log|*.tmp|*.cache|.env|.env.*|.DS_Store|Thumbs.db'
    else
        # Fallback to custom tree function
        echo "$(basename "$directory")/"
        generate_tree "$directory" "" true
    fi
} > project_structure.txt

# Search for sensitive information
echo "Scanning for sensitive information..."
{
    echo "=== Sensitive Information Scan ==="
    if grep -i -r --exclude="sensitive_info.txt" --exclude="project_info.txt" \
         --exclude-dir=".git" --exclude-dir="node_modules" --exclude-dir="__pycache__" \
         --exclude-dir="venv" --exclude-dir="env" --exclude-dir=".venv" \
         --exclude-dir="dist" --exclude-dir="build" --exclude-dir="target" \
         --exclude-dir="bin" --exclude-dir="obj" --exclude-dir=".next" \
         --exclude-dir=".nuxt" --exclude-dir="coverage" --exclude-dir=".pytest_cache" \
         --exclude-dir=".mypy_cache" --exclude="*.pyc" --exclude="*.pyo" \
         --exclude="*.class" --exclude="*.log" --exclude="*.tmp" \
         -E "(API_KEY|SECRET|PASSWORD|TOKEN|DATABASE_URL)" "$directory" 2>/dev/null; then
        echo ""
        echo "⚠️  WARNING: Potential sensitive information found above!"
    else
        echo "✅ No sensitive patterns found"
    fi
} > sensitive_info.txt

# Count lines of code for various file types
echo "Counting lines of code..."
{
    echo "=== Line Counts ==="
    
    # Find and count lines for each file type, excluding unnecessary directories and files
    total_lines=0
    file_count=0
    
    for file in $(find "$directory" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.tsx" \
                         -o -name "*.java" -o -name "*.c" -o -name "*.cpp" -o -name "*.sh" -o -name "*.go" \
                         -o -name "*.rb" -o -name "*.php" -o -name "*.html" -o -name "*.css" -o -name "*.scss" \
                         -o -name "*.json" -o -name "*.xml" -o -name "*.yaml" -o -name "*.yml" \) \
                         -not -path '*/node_modules/*' \
                         -not -path '*/__pycache__/*' \
                         -not -path '*/venv/*' \
                         -not -path '*/env/*' \
                         -not -path '*/.venv/*' \
                         -not -path '*/dist/*' \
                         -not -path '*/build/*' \
                         -not -path '*/target/*' \
                         -not -path '*/bin/*' \
                         -not -path '*/obj/*' \
                         -not -path '*/.next/*' \
                         -not -path '*/.nuxt/*' \
                         -not -path '*/coverage/*' \
                         -not -path '*/.pytest_cache/*' \
                         -not -path '*/.mypy_cache/*' \
                         -not -path '*/.git/*' \
                         2>/dev/null); do
        if [ -f "$file" ]; then
            lines=$(wc -l < "$file" 2>/dev/null || echo 0)
            echo "$lines $file"
            total_lines=$((total_lines + lines))
            file_count=$((file_count + 1))
        fi
    done
    
    echo ""
    echo "📊 Summary:"
    echo "Total files: $file_count"
    echo "Total lines: $total_lines"
    
    if [ $file_count -eq 0 ]; then
        echo "No code files found"
    fi
} > line_counts.txt

# Store project information
echo "Creating project_info.txt..."
{
    echo "=== PROJECT INFORMATION ==="
    echo "Generated on: $(date)"
    echo ""
    cat project_structure.txt
    echo ""
    cat sensitive_info.txt
    echo ""
    cat line_counts.txt
} > project_info.txt

echo "✅ Project information saved to project_info.txt"
echo "📁 Individual reports: project_structure.txt, sensitive_info.txt, line_counts.txt"
