"""
File utility functions for safe file operations.
"""

import os
import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


class FileUtils:
    """Utility class for file operations."""
    
    @staticmethod
    def read_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """Safely read a text file."""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except (FileNotFoundError, UnicodeDecodeError, OSError) as e:
            raise FileOperationError(f"Failed to read file {file_path}: {e}")
    
    @staticmethod
    def write_file(file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
        """Safely write content to a text file."""
        try:
            # Ensure directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
        except (OSError, UnicodeEncodeError) as e:
            raise FileOperationError(f"Failed to write file {file_path}: {e}")
    
    @staticmethod
    def append_file(file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
        """Safely append content to a text file."""
        try:
            # Ensure directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'a', encoding=encoding) as f:
                f.write(content)
        except (OSError, UnicodeEncodeError) as e:
            raise FileOperationError(f"Failed to append to file {file_path}: {e}")
    
    @staticmethod
    def read_json(file_path: Union[str, Path]) -> Dict[str, Any]:
        """Safely read a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
            raise FileOperationError(f"Failed to read JSON file {file_path}: {e}")
    
    @staticmethod
    def write_json(file_path: Union[str, Path], data: Dict[str, Any], indent: int = 2) -> None:
        """Safely write data to a JSON file."""
        try:
            # Ensure directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
        except (OSError, json.JSONEncodeError, TypeError) as e:
            raise FileOperationError(f"Failed to write JSON file {file_path}: {e}")
    
    @staticmethod
    def file_exists(file_path: Union[str, Path]) -> bool:
        """Check if a file exists."""
        return Path(file_path).exists()
    
    @staticmethod
    def directory_exists(dir_path: Union[str, Path]) -> bool:
        """Check if a directory exists."""
        return Path(dir_path).is_dir()
    
    @staticmethod
    def create_directory(dir_path: Union[str, Path]) -> None:
        """Create a directory if it doesn't exist."""
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise FileOperationError(f"Failed to create directory {dir_path}: {e}")
    
    @staticmethod
    def copy_file(source: Union[str, Path], destination: Union[str, Path]) -> None:
        """Copy a file from source to destination."""
        try:
            # Ensure destination directory exists
            Path(destination).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        except (OSError, shutil.Error) as e:
            raise FileOperationError(f"Failed to copy file from {source} to {destination}: {e}")
    
    @staticmethod
    def move_file(source: Union[str, Path], destination: Union[str, Path]) -> None:
        """Move a file from source to destination."""
        try:
            # Ensure destination directory exists
            Path(destination).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(source, destination)
        except (OSError, shutil.Error) as e:
            raise FileOperationError(f"Failed to move file from {source} to {destination}: {e}")
    
    @staticmethod
    def delete_file(file_path: Union[str, Path]) -> None:
        """Delete a file."""
        try:
            Path(file_path).unlink()
        except (OSError, FileNotFoundError) as e:
            raise FileOperationError(f"Failed to delete file {file_path}: {e}")
    
    @staticmethod
    def delete_directory(dir_path: Union[str, Path], recursive: bool = False) -> None:
        """Delete a directory."""
        try:
            if recursive:
                shutil.rmtree(dir_path)
            else:
                Path(dir_path).rmdir()
        except (OSError, shutil.Error) as e:
            raise FileOperationError(f"Failed to delete directory {dir_path}: {e}")
    
    @staticmethod
    def get_file_size(file_path: Union[str, Path]) -> int:
        """Get file size in bytes."""
        try:
            return Path(file_path).stat().st_size
        except OSError as e:
            raise FileOperationError(f"Failed to get size of file {file_path}: {e}")
    
    @staticmethod
    def get_file_modified_time(file_path: Union[str, Path]) -> datetime:
        """Get file modification time."""
        try:
            timestamp = Path(file_path).stat().st_mtime
            return datetime.fromtimestamp(timestamp)
        except OSError as e:
            raise FileOperationError(f"Failed to get modification time of file {file_path}: {e}")
    
    @staticmethod
    def list_files(dir_path: Union[str, Path], pattern: str = "*", recursive: bool = False) -> List[Path]:
        """List files in a directory matching a pattern."""
        try:
            dir_path = Path(dir_path)
            if recursive:
                return list(dir_path.rglob(pattern))
            else:
                return list(dir_path.glob(pattern))
        except OSError as e:
            raise FileOperationError(f"Failed to list files in directory {dir_path}: {e}")
    
    @staticmethod
    def backup_file(file_path: Union[str, Path], backup_dir: Optional[Union[str, Path]] = None) -> Path:
        """Create a backup of a file with timestamp."""
        file_path = Path(file_path)
        
        if backup_dir is None:
            backup_dir = file_path.parent / "backups"
        else:
            backup_dir = Path(backup_dir)
        
        # Create backup directory
        FileUtils.create_directory(backup_dir)
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = backup_dir / backup_name
        
        # Copy file to backup location
        FileUtils.copy_file(file_path, backup_path)
        
        return backup_path
    
    @staticmethod
    def read_lines(file_path: Union[str, Path], encoding: str = 'utf-8') -> List[str]:
        """Read file lines into a list."""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.readlines()
        except (FileNotFoundError, UnicodeDecodeError, OSError) as e:
            raise FileOperationError(f"Failed to read lines from file {file_path}: {e}")
    
    @staticmethod
    def write_lines(file_path: Union[str, Path], lines: List[str], encoding: str = 'utf-8') -> None:
        """Write lines to a file."""
        try:
            # Ensure directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.writelines(lines)
        except (OSError, UnicodeEncodeError) as e:
            raise FileOperationError(f"Failed to write lines to file {file_path}: {e}")
    
    @staticmethod
    def count_lines(file_path: Union[str, Path], encoding: str = 'utf-8') -> int:
        """Count lines in a file."""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return sum(1 for line in f)
        except (FileNotFoundError, UnicodeDecodeError, OSError) as e:
            raise FileOperationError(f"Failed to count lines in file {file_path}: {e}")
    
    @staticmethod
    def find_in_file(file_path: Union[str, Path], search_text: str, encoding: str = 'utf-8') -> List[int]:
        """Find line numbers containing search text."""
        try:
            line_numbers = []
            with open(file_path, 'r', encoding=encoding) as f:
                for line_num, line in enumerate(f, 1):
                    if search_text in line:
                        line_numbers.append(line_num)
            return line_numbers
        except (FileNotFoundError, UnicodeDecodeError, OSError) as e:
            raise FileOperationError(f"Failed to search in file {file_path}: {e}")
    
    @staticmethod
    def replace_in_file(file_path: Union[str, Path], old_text: str, new_text: str, 
                       encoding: str = 'utf-8') -> int:
        """Replace text in a file and return number of replacements."""
        try:
            content = FileUtils.read_file(file_path, encoding)
            new_content = content.replace(old_text, new_text)
            
            if content != new_content:
                FileUtils.write_file(file_path, new_content, encoding)
                return content.count(old_text)
            
            return 0
        except Exception as e:
            raise FileOperationError(f"Failed to replace text in file {file_path}: {e}")
    
    @staticmethod
    def get_current_timestamp() -> str:
        """Get current timestamp as string."""
        return datetime.now().isoformat()
    
    @staticmethod
    def get_file_extension(file_path: Union[str, Path]) -> str:
        """Get file extension."""
        return Path(file_path).suffix.lower()
    
    @staticmethod
    def get_file_name(file_path: Union[str, Path], with_extension: bool = True) -> str:
        """Get file name with or without extension."""
        path = Path(file_path)
        if with_extension:
            return path.name
        else:
            return path.stem
    
    @staticmethod
    def is_text_file(file_path: Union[str, Path]) -> bool:
        """Check if file is likely a text file based on extension."""
        text_extensions = {
            '.txt', '.md', '.rst', '.py', '.js', '.ts', '.tsx', '.jsx',
            '.html', '.css', '.scss', '.less', '.json', '.xml', '.yml',
            '.yaml', '.toml', '.ini', '.cfg', '.conf', '.log', '.sql',
            '.sh', '.bat', '.ps1', '.java', '.cpp', '.c', '.cs', '.go',
            '.rs', '.rb', '.php', '.swift', '.kt', '.dart', '.r', '.m'
        }
        
        extension = FileUtils.get_file_extension(file_path)
        return extension in text_extensions
    
    @staticmethod
    def safe_filename(filename: str) -> str:
        """Create a safe filename by removing/replacing invalid characters."""
        import re
        
        # Replace invalid characters with underscores
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Remove leading/trailing spaces and dots
        safe_name = safe_name.strip(' .')
        
        # Ensure it's not empty
        if not safe_name:
            safe_name = 'unnamed_file'
        
        return safe_name
    
    @staticmethod
    def get_relative_path(file_path: Union[str, Path], base_path: Union[str, Path]) -> Path:
        """Get relative path from base path."""
        try:
            return Path(file_path).relative_to(base_path)
        except ValueError:
            # File is not relative to base path
            return Path(file_path)
    
    @staticmethod
    def ensure_directory_exists(file_path: Union[str, Path]) -> None:
        """Ensure the directory for a file path exists."""
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)


class FileOperationError(Exception):
    """Exception raised for file operation errors."""
    pass