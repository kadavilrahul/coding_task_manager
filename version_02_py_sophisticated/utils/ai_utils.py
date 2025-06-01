"""
AI integration utilities for working with language models and AI services.
"""

import json
import re
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from datetime import datetime


class AIUtils:
    """Utility class for AI integration and prompt management."""
    
    @staticmethod
    def create_context_prompt(project_info: Dict[str, Any], current_task: Optional[str] = None) -> str:
        """Create a context prompt for AI assistants."""
        prompt_parts = [
            "# Project Context",
            f"Project: {project_info.get('project_name', 'Unknown')}",
            f"Type: {project_info.get('project_type', 'unknown')}",
            f"Description: {project_info.get('description', 'No description available')}",
        ]
        
        if project_info.get('tech_stack'):
            tech_stack = ', '.join(project_info['tech_stack'])
            prompt_parts.append(f"Technology Stack: {tech_stack}")
        
        if project_info.get('architecture'):
            prompt_parts.append(f"Architecture: {project_info['architecture']}")
        
        prompt_parts.extend([
            "",
            "# Guidelines",
            "- Follow established coding standards",
            "- Write clean, maintainable code",
            "- Include comprehensive error handling",
            "- Add appropriate comments and documentation",
            "- Consider security best practices",
            "- Optimize for performance when relevant"
        ])
        
        if current_task:
            prompt_parts.extend([
                "",
                f"# Current Task",
                current_task
            ])
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def create_code_review_prompt(code: str, language: str, focus_areas: Optional[List[str]] = None) -> str:
        """Create a prompt for code review."""
        prompt_parts = [
            "# Code Review Request",
            f"Language: {language}",
            "",
            "Please review the following code and provide feedback on:"
        ]
        
        if focus_areas:
            for area in focus_areas:
                prompt_parts.append(f"- {area}")
        else:
            prompt_parts.extend([
                "- Code quality and readability",
                "- Performance optimizations",
                "- Security considerations",
                "- Best practices adherence",
                "- Potential bugs or issues",
                "- Documentation and comments"
            ])
        
        prompt_parts.extend([
            "",
            "# Code to Review",
            f"```{language}",
            code,
            "```",
            "",
            "Please provide specific, actionable feedback with examples where appropriate."
        ])
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def create_implementation_prompt(task_description: str, requirements: List[str], 
                                   context: Optional[Dict[str, Any]] = None) -> str:
        """Create a prompt for implementing a feature or task."""
        prompt_parts = [
            "# Implementation Request",
            f"Task: {task_description}",
            "",
            "# Requirements"
        ]
        
        for i, req in enumerate(requirements, 1):
            prompt_parts.append(f"{i}. {req}")
        
        if context:
            prompt_parts.extend([
                "",
                "# Context"
            ])
            
            for key, value in context.items():
                if isinstance(value, (list, dict)):
                    value = json.dumps(value, indent=2)
                prompt_parts.append(f"{key}: {value}")
        
        prompt_parts.extend([
            "",
            "# Expected Output",
            "Please provide:",
            "1. Complete, working code implementation",
            "2. Explanation of the approach",
            "3. Any assumptions made",
            "4. Testing recommendations",
            "5. Documentation for the implementation"
        ])
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def create_debugging_prompt(error_message: str, code_snippet: str, 
                              language: str, context: Optional[str] = None) -> str:
        """Create a prompt for debugging assistance."""
        prompt_parts = [
            "# Debugging Request",
            f"Language: {language}",
            "",
            "# Error Message",
            f"```",
            error_message,
            "```",
            "",
            "# Code Snippet",
            f"```{language}",
            code_snippet,
            "```"
        ]
        
        if context:
            prompt_parts.extend([
                "",
                "# Additional Context",
                context
            ])
        
        prompt_parts.extend([
            "",
            "# Request",
            "Please help debug this issue by:",
            "1. Identifying the root cause of the error",
            "2. Providing a corrected version of the code",
            "3. Explaining what was wrong and why",
            "4. Suggesting ways to prevent similar issues"
        ])
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def create_refactoring_prompt(code: str, language: str, goals: List[str]) -> str:
        """Create a prompt for code refactoring."""
        prompt_parts = [
            "# Refactoring Request",
            f"Language: {language}",
            "",
            "# Refactoring Goals"
        ]
        
        for i, goal in enumerate(goals, 1):
            prompt_parts.append(f"{i}. {goal}")
        
        prompt_parts.extend([
            "",
            "# Current Code",
            f"```{language}",
            code,
            "```",
            "",
            "# Request",
            "Please refactor this code to achieve the stated goals while:",
            "- Maintaining the same functionality",
            "- Improving code quality and readability",
            "- Following best practices",
            "- Adding appropriate comments",
            "",
            "Please provide the refactored code and explain the changes made."
        ])
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def extract_code_blocks(text: str) -> List[Dict[str, str]]:
        """Extract code blocks from AI response text."""
        code_blocks = []
        
        # Pattern to match code blocks with optional language specification
        pattern = r'```(\w+)?\n(.*?)\n```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        for language, code in matches:
            code_blocks.append({
                'language': language or 'text',
                'code': code.strip()
            })
        
        return code_blocks
    
    @staticmethod
    def extract_suggestions(text: str) -> List[str]:
        """Extract suggestions or recommendations from AI response."""
        suggestions = []
        
        # Look for numbered lists
        numbered_pattern = r'^\d+\.\s+(.+)$'
        # Look for bullet points
        bullet_pattern = r'^[-*]\s+(.+)$'
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Check for numbered suggestions
            numbered_match = re.match(numbered_pattern, line)
            if numbered_match:
                suggestions.append(numbered_match.group(1))
                continue
            
            # Check for bullet point suggestions
            bullet_match = re.match(bullet_pattern, line)
            if bullet_match:
                suggestions.append(bullet_match.group(1))
        
        return suggestions
    
    @staticmethod
    def format_prompt_for_model(prompt: str, model_type: str = "gemini") -> str:
        """Format prompt for specific AI model requirements."""
        if model_type.lower() == "gemini":
            # Gemini-specific formatting
            return AIUtils._format_for_gemini(prompt)
        elif model_type.lower() in ["gpt", "openai"]:
            # OpenAI GPT formatting
            return AIUtils._format_for_gpt(prompt)
        else:
            # Generic formatting
            return prompt
    
    @staticmethod
    def _format_for_gemini(prompt: str) -> str:
        """Format prompt for Gemini API."""
        # Gemini works well with structured prompts
        # Add clear sections and formatting
        formatted_prompt = prompt
        
        # Ensure clear section headers
        formatted_prompt = re.sub(r'^# (.+)$', r'## \1', formatted_prompt, flags=re.MULTILINE)
        
        return formatted_prompt
    
    @staticmethod
    def _format_for_gpt(prompt: str) -> str:
        """Format prompt for OpenAI GPT models."""
        # GPT models work well with conversational style
        return prompt
    
    @staticmethod
    def estimate_token_count(text: str, model_type: str = "gemini") -> int:
        """Estimate token count for a given text."""
        # Rough estimation: 1 token ≈ 4 characters for most models
        # This is a simplified estimation
        
        if model_type.lower() == "gemini":
            # Gemini token estimation
            return len(text) // 4
        elif model_type.lower() in ["gpt", "openai"]:
            # GPT token estimation (slightly different)
            return len(text.split()) * 1.3  # Words * average tokens per word
        else:
            # Generic estimation
            return len(text) // 4
    
    @staticmethod
    def optimize_prompt_length(prompt: str, max_tokens: int = 4000, model_type: str = "gemini") -> str:
        """Optimize prompt length to fit within token limits."""
        current_tokens = AIUtils.estimate_token_count(prompt, model_type)
        
        if current_tokens <= max_tokens:
            return prompt
        
        # If prompt is too long, try to shorten it
        lines = prompt.split('\n')
        
        # Keep essential sections (headers and first few lines)
        essential_lines = []
        optional_lines = []
        
        for line in lines:
            if line.startswith('#') or line.startswith('##'):
                essential_lines.append(line)
            elif len(essential_lines) < 10:  # Keep first 10 lines as essential
                essential_lines.append(line)
            else:
                optional_lines.append(line)
        
        # Start with essential lines and add optional ones until we hit the limit
        optimized_prompt = '\n'.join(essential_lines)
        
        for line in optional_lines:
            test_prompt = optimized_prompt + '\n' + line
            if AIUtils.estimate_token_count(test_prompt, model_type) > max_tokens:
                break
            optimized_prompt = test_prompt
        
        return optimized_prompt
    
    @staticmethod
    def create_file_context(file_path: Path, max_lines: int = 50) -> str:
        """Create context information for a file."""
        try:
            from .file_utils import FileUtils
            
            if not FileUtils.file_exists(file_path):
                return f"File {file_path} does not exist."
            
            # Get file info
            file_size = FileUtils.get_file_size(file_path)
            modified_time = FileUtils.get_file_modified_time(file_path)
            
            context_parts = [
                f"File: {file_path}",
                f"Size: {file_size} bytes",
                f"Modified: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}",
                ""
            ]
            
            # Add file content (limited)
            if FileUtils.is_text_file(file_path):
                try:
                    lines = FileUtils.read_lines(file_path)
                    total_lines = len(lines)
                    
                    if total_lines <= max_lines:
                        context_parts.append("Content:")
                        context_parts.extend([f"{i+1:3d}: {line.rstrip()}" for i, line in enumerate(lines)])
                    else:
                        context_parts.append(f"Content (first {max_lines} of {total_lines} lines):")
                        context_parts.extend([f"{i+1:3d}: {line.rstrip()}" for i, line in enumerate(lines[:max_lines])])
                        context_parts.append(f"... ({total_lines - max_lines} more lines)")
                
                except Exception as e:
                    context_parts.append(f"Error reading file content: {e}")
            else:
                context_parts.append("Binary file - content not shown")
            
            return '\n'.join(context_parts)
        
        except Exception as e:
            return f"Error creating file context: {e}"
    
    @staticmethod
    def create_project_summary(project_info: Dict[str, Any], file_list: List[Path]) -> str:
        """Create a summary of the project for AI context."""
        summary_parts = [
            "# Project Summary",
            f"Name: {project_info.get('project_name', 'Unknown')}",
            f"Type: {project_info.get('project_type', 'unknown')}",
            f"Description: {project_info.get('description', 'No description')}",
        ]
        
        if project_info.get('tech_stack'):
            summary_parts.append(f"Tech Stack: {', '.join(project_info['tech_stack'])}")
        
        summary_parts.extend([
            "",
            "# File Structure"
        ])
        
        # Group files by directory
        directories = {}
        for file_path in file_list:
            dir_name = str(file_path.parent)
            if dir_name not in directories:
                directories[dir_name] = []
            directories[dir_name].append(file_path.name)
        
        for dir_name, files in sorted(directories.items()):
            summary_parts.append(f"{dir_name}/")
            for file_name in sorted(files):
                summary_parts.append(f"  {file_name}")
        
        return '\n'.join(summary_parts)
    
    @staticmethod
    def validate_ai_response(response: str, expected_format: str = "code") -> Dict[str, Any]:
        """Validate AI response format and extract relevant information."""
        validation_result = {
            'valid': True,
            'issues': [],
            'extracted_data': {}
        }
        
        if expected_format == "code":
            code_blocks = AIUtils.extract_code_blocks(response)
            if not code_blocks:
                validation_result['valid'] = False
                validation_result['issues'].append("No code blocks found in response")
            else:
                validation_result['extracted_data']['code_blocks'] = code_blocks
        
        elif expected_format == "suggestions":
            suggestions = AIUtils.extract_suggestions(response)
            if not suggestions:
                validation_result['valid'] = False
                validation_result['issues'].append("No suggestions found in response")
            else:
                validation_result['extracted_data']['suggestions'] = suggestions
        
        # Check for common issues
        if len(response.strip()) < 10:
            validation_result['valid'] = False
            validation_result['issues'].append("Response too short")
        
        return validation_result