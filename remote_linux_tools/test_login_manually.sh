#!/bin/bash

# Default credentials
DEFAULT_IP=""
DEFAULT_USER="root"
DEFAULT_PASS=""
DEFAULT_PORT="22"

# Clear screen for better visibility
clear

echo "=== SSH Login Script ==="
echo "Press Enter to use default values or input new ones"
echo -e "Default IP: $DEFAULT_IP\n"

# Get server details with defaults
read -p "Enter server IP/hostname [$DEFAULT_IP]: " server_host
server_host=${server_host:-$DEFAULT_IP}

read -p "Enter username [$DEFAULT_USER]: " server_user
server_user=${server_user:-$DEFAULT_USER}

read -p "Enter port [$DEFAULT_PORT]: " server_port
server_port=${server_port:-$DEFAULT_PORT}

# Password prompt with default option
read -p "Use default password? (y/N): " use_default_pass
use_default_pass=${use_default_pass:-N}

if [[ "${use_default_pass,,}" == "y" ]]; then
    server_pass="$DEFAULT_PASS"
else
    # -s flag hides password input
    read -s -p "Enter password: " server_pass
    echo
fi

# Use sshpass for password-based login
if ! command -v sshpass &> /dev/null; then
    echo "Installing sshpass..."
    sudo apt-get install sshpass -y
fi

echo -e "\nConnecting to $server_host as $server_user..."
sshpass -p "$server_pass" ssh -o StrictHostKeyChecking=no -p "$server_port" "$server_user@$server_host"