# File Versioning System with inotify

A lightweight file versioning system that automatically creates backups of files when they are modified, using Linux's inotify for file system monitoring.

## Features
- Real-time file change monitoring using inotify
- Automatic timestamped backups
- Monitors current directory and subdirectories
- Simple process management with PID tracking
- Easy to use start/stop/status commands
- Non-intrusive background operation
- Useful in working with AI-based code editors
- It makes sure that your code is always backed up after code editor makes changes

## Prerequisites
- Linux system with inotify-tools installed
# Ubuntu/Debian
```bash
sudo apt-get install inotify-tools
```
# CentOS/RHEL
```bash
sudo yum install inotify-tools
```

## Installation

### Option 1: Quick Setup (Recommended)
For quick setup in your target directory:

1. Go to the directory one level up of the directory to be watched so that files and backups are not created in the project directory.

2. Copy the scripts from this directory to your target directory:
```bash
cp path/to/scripts_04/{setup_file_versioning.sh,file_versioning.sh,check_versioning.sh} .
```

3. Run the setup script:
```bash
bash setup_file_versioning.sh
```

4. Start the file versioning system:
```bash
nohup bash file_versioning.sh > file_versioning.log 2>&1 &
```

5. Check Status:
```bash
bash check_versioning.sh
```

6. Stop File Versioning:
```bash
pkill -f file_versioning.sh
```

This setup will:
1. Copy the necessary scripts to your current directory
2. Make them executable
3. Update .gitignore to exclude versioning files
4. Start monitoring your directory for file changes

### Option 2: Manual Installation
1. Navigate to the directory you want to monitor:
```bash
cd /path/to/your/directory  # Replace with the directory you want to monitor
```

2. Copy the scripts from the scripts_04 directory:
```bash
cp /path/to/scripts_04/{setup_file_versioning.sh,file_versioning.sh,check_versioning.sh} .
```

3. Make the scripts executable:
```bash
chmod +x setup_file_versioning.sh file_versioning.sh check_versioning.sh
```

## Usage

1. Start File Versioning (will monitor current directory and sub directories):
```bash
nohup bash file_versioning.sh > file_versioning.log 2>&1 &
```

2. Check Status:
```bash
bash check_versioning.sh
```

3. Stop File Versioning:
```bash
pkill -f file_versioning.sh
```

## File Organization
- `file_versioning.sh`: Main script that monitors and creates backups
- `check_versioning.sh`: Helper script to check if the versioning system is running
- `setup_file_versioning.sh`: Setup script that copies files and configures .gitignore
- `backups/`: Directory where backups are stored (created automatically)
- `.file_versioning.pid`: PID file for process management (created automatically)
- `.versioningignore`: Configuration file to specify which files to ignore (created automatically)

## Backup Format
- Backups are stored in the `backups` directory
- Naming format: `original_filename_YYYY_MM_DD_HH:MM:SS`
- Example: `document.txt_2025_02_01_14:53:51`

## Configuration
Edit `file_versioning.sh` to customize:
- `WATCH_DIR`: Directory to monitor (default: script location)
- `BACKUP_DIR`: Directory for storing backups (default: backups/ subdirectory)

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
MIT License - feel free to use and modify as needed.

## Author
[Rahul Dinesh]
