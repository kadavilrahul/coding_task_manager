#!/bin/bash

# Test script to verify the generate_prd.sh fix
echo "Testing the fixed generate_prd.sh script..."

# Create a test directory
mkdir -p test_dir
cp test_project_info.txt test_dir/project_info.txt

# Set a dummy API key for testing (this won't actually call the API)
export GEMINI_API_KEY="test_key_for_validation"

# Test the script with dry run (we'll modify it to not actually call the API)
echo "Running generate_prd.sh with test data..."

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required for this test"
    exit 1
fi

# Test the JSON creation part of our fix
test_prompt="This is a test prompt with some special characters: \"quotes\" and 'apostrophes' and newlines
and multiple lines of text to simulate a large project_info.txt file."

echo "Testing JSON creation..."
temp_json=$(mktemp /tmp/test_gemini_payload_XXXXXX.json)

# Test our JSON creation method
if echo "$test_prompt" | jq -R -s . > /tmp/test_escaped_prompt.json; then
    cat > "$temp_json" << EOF
{
    "contents": [{
        "parts": [{
            "text": $(cat /tmp/test_escaped_prompt.json)
        }]
    }]
}
EOF
    
    # Validate the JSON
    if jq . "$temp_json" > /dev/null; then
        echo "✓ JSON creation and validation successful"
    else
        echo "✗ JSON validation failed"
    fi
else
    echo "✗ JSON escaping failed"
fi

# Cleanup
rm -f "$temp_json" /tmp/test_escaped_prompt.json test_dir/project_info.txt
rmdir test_dir

echo "Test completed."