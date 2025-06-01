"""
Pytest configuration and fixtures for the AI-Enhanced Task Management System.
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any
import json

from core.task_manager import TaskManager
from core.prd_generator import PRDGenerator
from agents.analyzer_agent import AnalyzerAgent
from agents.planner_agent import PlannerAgent
from agents.modifier_agent import ModifierAgent
from agents.validator_agent import ValidatorAgent


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_config():
    """Provide a sample configuration for testing."""
    return {
        "task_manager": {
            "max_concurrent_tasks": 3,
            "task_timeout": 60,
            "auto_save": False,
            "storage_backend": "memory"
        },
        "ai_utils": {
            "provider": "mock",
            "model": "test-model",
            "temperature": 0.5,
            "max_tokens": 1000
        },
        "analyzer_agent": {
            "analysis_depth": "basic",
            "include_metrics": False,
            "complexity_threshold": 5
        }
    }


@pytest.fixture
def sample_python_file(temp_dir):
    """Create a sample Python file for testing."""
    file_path = temp_dir / "sample.py"
    content = '''
"""Sample Python module for testing."""

import os
import sys
from typing import List, Dict, Any


class SampleClass:
    """A sample class for testing."""
    
    def __init__(self, name: str):
        """Initialize the sample class."""
        self.name = name
        self._private_attr = 0
    
    def public_method(self, value: int) -> int:
        """A public method."""
        return value * 2
    
    def _private_method(self) -> str:
        """A private method."""
        return f"Private: {self.name}"


def sample_function(items: List[str]) -> Dict[str, Any]:
    """A sample function for testing."""
    result = {}
    for i, item in enumerate(items):
        result[f"item_{i}"] = {
            "value": item,
            "length": len(item),
            "upper": item.upper()
        }
    return result


async def async_function(delay: float = 1.0) -> str:
    """An async function for testing."""
    await asyncio.sleep(delay)
    return "async_result"


def complex_function(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """A more complex function for testing."""
    results = []
    
    for key, value in data.items():
        if isinstance(value, (int, float)):
            results.append({
                "key": key,
                "value": value,
                "squared": value ** 2,
                "type": "numeric"
            })
        elif isinstance(value, str):
            results.append({
                "key": key,
                "value": value,
                "length": len(value),
                "type": "string"
            })
        else:
            results.append({
                "key": key,
                "value": str(value),
                "type": "other"
            })
    
    return sorted(results, key=lambda x: x["key"])


if __name__ == "__main__":
    # Sample usage
    obj = SampleClass("test")
    print(obj.public_method(5))
    
    items = ["hello", "world", "test"]
    result = sample_function(items)
    print(result)
'''
    
    file_path.write_text(content)
    return file_path


@pytest.fixture
def task_manager(sample_config):
    """Create a TaskManager instance for testing."""
    return TaskManager(sample_config)


@pytest.fixture
def prd_generator(sample_config):
    """Create a PRDGenerator instance for testing."""
    return PRDGenerator(sample_config)


@pytest.fixture
def analyzer_agent(sample_config):
    """Create an AnalyzerAgent instance for testing."""
    return AnalyzerAgent(sample_config)


@pytest.fixture
def planner_agent(sample_config):
    """Create a PlannerAgent instance for testing."""
    return PlannerAgent(sample_config)


@pytest.fixture
def modifier_agent(sample_config):
    """Create a ModifierAgent instance for testing."""
    return ModifierAgent(sample_config)


@pytest.fixture
def validator_agent(sample_config):
    """Create a ValidatorAgent instance for testing."""
    return ValidatorAgent(sample_config)


@pytest.fixture
def sample_task():
    """Provide a sample task for testing."""
    return {
        "id": "test-task-001",
        "title": "Implement user authentication",
        "description": "Add secure user login and registration functionality",
        "priority": "high",
        "status": "pending",
        "requirements": [
            "User registration with email validation",
            "Secure password hashing using bcrypt",
            "JWT token-based authentication",
            "Password reset functionality",
            "User profile management"
        ],
        "estimated_hours": 16,
        "tags": ["authentication", "security", "backend"],
        "dependencies": [],
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_project_info():
    """Provide sample project information for testing."""
    return {
        "title": "E-commerce Platform",
        "description": "A modern e-commerce platform with AI-powered recommendations",
        "version": "1.0.0",
        "objectives": [
            "Create a scalable e-commerce platform",
            "Implement AI-powered product recommendations",
            "Ensure secure payment processing",
            "Provide excellent user experience"
        ],
        "requirements": [
            "User authentication and authorization",
            "Product catalog management",
            "Shopping cart functionality",
            "Payment processing integration",
            "Order management system",
            "AI recommendation engine",
            "Admin dashboard",
            "Mobile-responsive design"
        ],
        "tech_stack": [
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Redis",
            "React",
            "TypeScript"
        ],
        "target_audience": "Online shoppers and business owners",
        "success_criteria": [
            "Handle 10,000+ concurrent users",
            "99.9% uptime",
            "Sub-2 second page load times",
            "Secure payment processing"
        ]
    }


@pytest.fixture
def mock_ai_response():
    """Provide mock AI responses for testing."""
    return {
        "analysis": {
            "summary": "This is a mock analysis response",
            "complexity": "medium",
            "suggestions": ["Add error handling", "Improve documentation"]
        },
        "plan": {
            "tasks": [
                {"id": 1, "title": "Setup project structure", "estimated_hours": 2},
                {"id": 2, "title": "Implement core functionality", "estimated_hours": 8},
                {"id": 3, "title": "Add tests", "estimated_hours": 4}
            ],
            "total_hours": 14
        },
        "code": {
            "content": "# Generated code\nprint('Hello, World!')",
            "language": "python",
            "explanation": "This is a simple hello world example"
        }
    }