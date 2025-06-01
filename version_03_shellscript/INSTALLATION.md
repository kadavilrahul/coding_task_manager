# Installation Guide

This guide provides commands to install and run the Agno Code Tools.

1.  **Install Git, jq, and Curl:**

    ```bash
    sudo apt update && sudo apt install git jq curl  # Debian/Ubuntu
    sudo dnf install git jq curl              # Fedora/CentOS/RHEL
    ```

2.  **Set up the Gemini API key:**

    *   Get a Gemini API key
    *   Set the `GEMINI_API_KEY` environment variable:
        (Replace `"YOUR_GEMINI_API_KEY"` with your actual Gemini API key)
        
        ```bash
        export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        ```

        You can check by running below command in your terminal.
        ```bash
        echo $GEMINI_API_KEY
        ```
        
        
3.  **Download the code:**

    ```bash
    git clone <repository_url>
    cd agno-code-tools
    ```

    (Replace `<repository_url>` with the URL of this repository)

4.  **Make the scripts executable:**

    ```bash
    chmod +x *.sh
    ```

5.  **Run the project info script:**

    ```bash
    ./project_info.sh
    ```

    (Enter a brief description of the project when prompted)

6.  **Use other scripts as needed:**

    ```bash
    ./file_paths.sh
    ./extract_functions.sh
    ./modify_code.sh
    ./identify_changes.sh
    ./join_code.sh