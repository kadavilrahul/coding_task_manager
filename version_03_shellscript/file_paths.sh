#!/bin/bash

# List all files
find . -type f > file_list.txt

# Prompt for file name or pattern
read -p "Enter a file name or pattern: " file_pattern

# Filter file list
grep "$file_pattern" file_list.txt

# Clean up
rm file_list.txt