# Flowchart Generator

## Overview
A streamlined setup for generating flowcharts in HTML and PNG formats. This tool helps automate the process of creating flowcharts, making it particularly useful for AI workflows and documentation.

## Features
- Command line based flowchart generation environment
- Automated dependency management and setup
- HTML and PNG output formats
- Easy-to-use command line interface
- Automatic environment configuration

## System Requirements
- Linux system with GUI (GUI needed to view files)
- Tested on Ubuntu 24.04 LTS

**Note:** This setup should work on most other Linux distributions with minimal modifications. For headless servers, ensure you have GUI access through a remote desktop solution.

## Installation & Usage

### First time setup:
```bash
cd flowchart_generator
bash setup_flowchart.sh
```

### Subsequent runs:
```bash
bash generate.sh
```

### Alternative Setup (move to project root):
```bash
# Move files to current directory where other scripts are present
mv setup_flowchart.sh generate.sh ../
cd ..
bash setup_flowchart.sh
```

## Workflow
1. Run the setup script for first-time installation
2. Follow on-screen prompts for initial setup preferences
3. Specify task requirements when prompted
4. The tool will automatically:
   - Set up the required environment
   - Install dependencies
   - Generate flowcharts

## Troubleshooting
- Ensure all system requirements are met
- Check your internet connection
- Make sure GUI access is available
- Verify that all dependencies are properly installed

## Integration
This tool integrates seamlessly with the other script collections in the coding task manager, particularly useful for:
- Documenting AI workflows
- Creating visual representations of project structures
- Generating process diagrams for development workflows

## Contributing
Feel free to contribute to this project by:
- Submitting bug reports
- Proposing new features
- Creating pull requests

## License
This project is open source and available under the MIT License.
