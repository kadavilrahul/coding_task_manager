#!/bin/bash
# This script automates the execution of remote commands on a server using SSH.
# It allows defining a list of commands and default server credentials, and executes the commands on the remote server.

# Insert your credentials below before execution the script

# Default credentials
DEFAULT_USER=""
DEFAULT_PORT=""
DEFAULT_IP=""
DEFAULT_PASS=""

# Set server details to defaults
server_host="$DEFAULT_IP"
server_user="$DEFAULT_USER"
server_port="$DEFAULT_PORT"
server_pass="$DEFAULT_PASS"

# Define your commands here
# Add or remove commands as needed
commands=(
    "sudo apt update"
    "df -h"
    "free -m"
    "uptime"
    "ls -la"
    # Add more commands below
    # "your_command_here"
)

# Check if sshpass is installed
if ! command -v sshpass &> /dev/null; then
    echo "Installing sshpass..."
    sudo apt-get install sshpass -y
fi

# Function to execute remote commands
execute_remote_command() {
    sshpass -p "$server_pass" ssh -o StrictHostKeyChecking=no -p "$server_port" "$server_user@$server_host" "$1"
}

# Main execution
echo -e "\n=== Remote Server Command Execution ==="
echo "Server: $server_host"
echo "User: $server_user"
echo "Port: $server_port"
echo "Password: [using default]"

# Show summary of commands to be executed
echo -e "\nCommands to be executed:"
for ((i=0; i<${#commands[@]}; i++)); do
    echo "$((i+1)). ${commands[i]}"
done

echo -e "\nExecuting commands..."
# Execute each command
for cmd in "${commands[@]}"; do
    echo -e "\nExecuting: $cmd"
    execute_remote_command "$cmd"
    echo "------------------------"
done

echo "All commands executed successfully!"
