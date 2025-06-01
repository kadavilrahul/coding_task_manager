#!/bin/bash

# Get file paths
original_file="$1"
modified_file="$2"

# Use diff to identify changes
diff "$original_file" "$modified_file"