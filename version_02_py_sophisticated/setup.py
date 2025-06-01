"""
Setup script for the AI-Enhanced Task Management System.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith('#') and not line.startswith('-')
        ]

setup(
    name="ai-task-management",
    version="2.0.0",
    author="AI Assistant",
    author_email="ai@example.com",
    description="An AI-enhanced task management system for software development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/ai-task-management",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Documentation",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.4.0",
            "pre-commit>=3.3.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
        "api": [
            "fastapi>=0.100.0",
            "uvicorn>=0.20.0",
        ],
        "database": [
            "sqlalchemy>=2.0.0",
            "alembic>=1.11.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-task-manager=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.yaml", "*.yml", "*.md", "*.txt"],
        "templates": ["*.md", "*.py", "*.js", "*.html"],
    },
    zip_safe=False,
    keywords=[
        "ai",
        "task-management",
        "software-development",
        "automation",
        "code-analysis",
        "documentation",
        "planning",
    ],
    project_urls={
        "Bug Reports": "https://github.com/example/ai-task-management/issues",
        "Source": "https://github.com/example/ai-task-management",
        "Documentation": "https://ai-task-management.readthedocs.io/",
    },
)