# Remote Linux Tools

## Overview
A collection of shell scripts for automated remote Linux server login and command execution. These tools provide secure, configurable ways to interact with remote servers through SSH.

## Script Contents
- `main.sh` - Main automation script for remote command execution
- `test_login_manually.sh` - Interactive login testing script
- `test_run_commands_with_manual_login.sh` - Combined login and command execution test

## Features
- **Secure SSH Authentication**: Multiple authentication methods supported
- **Automated Command Execution**: Execute commands on remote servers automatically
- **Configurable Settings**: Easy-to-configure remote server parameters
- **Error Handling**: Robust error handling and validation
- **Interactive Testing**: Manual testing capabilities for debugging
- **Batch Operations**: Support for running multiple commands

## Prerequisites
- Linux/Unix environment
- SSH access to remote server
- Proper SSH key configuration (recommended)
- Basic networking knowledge

## Configuration

### Setup Credentials
Before running the automation script, configure the following variables in `main.sh`:

```bash
DEFAULT_USER="your_username"
DEFAULT_PORT="22"
DEFAULT_IP="remote_server_ip"
DEFAULT_PASS="your_password"  # Not recommended - use SSH keys instead
```

## Usage

### Automated Execution
```bash
cd remote_linux_tools
bash main.sh
```

### Interactive Testing
```bash
# Test login functionality
bash test_login_manually.sh

# Test command execution with manual login
bash test_run_commands_with_manual_login.sh
```

## Security Best Practices

**⚠️ Important Security Notes:**
- **Never store sensitive credentials in scripts**
- **Use SSH keys for authentication instead of passwords**
- **Set proper file permissions** (600 for scripts with credentials)
- **Review automated commands before execution**
- **Use dedicated service accounts** for automation
- **Enable SSH logging** for audit trails

### SSH Key Setup (Recommended)
```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_remote

# Copy public key to remote server
ssh-copy-id -i ~/.ssh/id_rsa_remote.pub user@remote_server

# Configure SSH to use key
ssh -i ~/.ssh/id_rsa_remote user@remote_server
```

## Troubleshooting
- **Connection refused**: Check SSH service status and firewall settings
- **Authentication failed**: Verify credentials and SSH key configuration
- **Permission denied**: Check file permissions and SSH server configuration
- **Command not found**: Verify PATH and command availability on remote server

## Integration
This script collection integrates with the coding task manager for:
- Remote deployment workflows
- Automated testing on remote servers
- Distributed development environments
- Remote backup and maintenance tasks

## License
This project is open source and available under the MIT License.

