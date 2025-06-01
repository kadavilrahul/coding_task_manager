"""
Tests for the TaskManager class.
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, patch

from core.task_manager import TaskManager, TaskStatus, TaskPriority


class TestTaskManager:
    """Test cases for TaskManager."""

    @pytest.mark.asyncio
    async def test_create_task(self, task_manager, sample_task):
        """Test task creation."""
        # Remove id from sample task as it should be auto-generated
        task_data = sample_task.copy()
        del task_data['id']
        
        created_task = await task_manager.create_task(task_data)
        
        assert created_task is not None
        assert 'id' in created_task
        assert created_task['title'] == task_data['title']
        assert created_task['status'] == TaskStatus.PENDING.value
        assert created_task['priority'] == TaskPriority.HIGH.value

    @pytest.mark.asyncio
    async def test_get_task(self, task_manager, sample_task):
        """Test task retrieval."""
        # Create a task first
        task_data = sample_task.copy()
        del task_data['id']
        created_task = await task_manager.create_task(task_data)
        
        # Retrieve the task
        retrieved_task = await task_manager.get_task(created_task['id'])
        
        assert retrieved_task is not None
        assert retrieved_task['id'] == created_task['id']
        assert retrieved_task['title'] == created_task['title']

    @pytest.mark.asyncio
    async def test_update_task(self, task_manager, sample_task):
        """Test task update."""
        # Create a task first
        task_data = sample_task.copy()
        del task_data['id']
        created_task = await task_manager.create_task(task_data)
        
        # Update the task
        updates = {
            'title': 'Updated Task Title',
            'status': TaskStatus.IN_PROGRESS.value,
            'priority': TaskPriority.MEDIUM.value
        }
        
        updated_task = await task_manager.update_task(created_task['id'], updates)
        
        assert updated_task is not None
        assert updated_task['title'] == updates['title']
        assert updated_task['status'] == updates['status']
        assert updated_task['priority'] == updates['priority']

    @pytest.mark.asyncio
    async def test_delete_task(self, task_manager, sample_task):
        """Test task deletion."""
        # Create a task first
        task_data = sample_task.copy()
        del task_data['id']
        created_task = await task_manager.create_task(task_data)
        
        # Delete the task
        result = await task_manager.delete_task(created_task['id'])
        
        assert result is True
        
        # Verify task is deleted
        deleted_task = await task_manager.get_task(created_task['id'])
        assert deleted_task is None

    @pytest.mark.asyncio
    async def test_list_tasks(self, task_manager, sample_task):
        """Test task listing."""
        # Create multiple tasks
        task_data = sample_task.copy()
        del task_data['id']
        
        tasks = []
        for i in range(3):
            task_copy = task_data.copy()
            task_copy['title'] = f"Task {i+1}"
            created_task = await task_manager.create_task(task_copy)
            tasks.append(created_task)
        
        # List all tasks
        all_tasks = await task_manager.list_tasks()
        
        assert len(all_tasks) >= 3
        task_titles = [task['title'] for task in all_tasks]
        assert "Task 1" in task_titles
        assert "Task 2" in task_titles
        assert "Task 3" in task_titles

    @pytest.mark.asyncio
    async def test_list_tasks_with_filter(self, task_manager, sample_task):
        """Test task listing with filters."""
        # Create tasks with different statuses
        task_data = sample_task.copy()
        del task_data['id']
        
        # Create pending task
        pending_task_data = task_data.copy()
        pending_task_data['title'] = "Pending Task"
        pending_task_data['status'] = TaskStatus.PENDING.value
        await task_manager.create_task(pending_task_data)
        
        # Create in-progress task
        in_progress_task_data = task_data.copy()
        in_progress_task_data['title'] = "In Progress Task"
        in_progress_task_data['status'] = TaskStatus.IN_PROGRESS.value
        await task_manager.create_task(in_progress_task_data)
        
        # Filter by status
        pending_tasks = await task_manager.list_tasks(
            filters={'status': TaskStatus.PENDING.value}
        )
        
        assert len(pending_tasks) >= 1
        for task in pending_tasks:
            assert task['status'] == TaskStatus.PENDING.value

    @pytest.mark.asyncio
    async def test_get_task_statistics(self, task_manager, sample_task):
        """Test task statistics retrieval."""
        # Create tasks with different statuses and priorities
        task_data = sample_task.copy()
        del task_data['id']
        
        # Create multiple tasks
        for i in range(5):
            task_copy = task_data.copy()
            task_copy['title'] = f"Stats Task {i+1}"
            if i < 2:
                task_copy['status'] = TaskStatus.PENDING.value
                task_copy['priority'] = TaskPriority.HIGH.value
            elif i < 4:
                task_copy['status'] = TaskStatus.IN_PROGRESS.value
                task_copy['priority'] = TaskPriority.MEDIUM.value
            else:
                task_copy['status'] = TaskStatus.COMPLETED.value
                task_copy['priority'] = TaskPriority.LOW.value
            
            await task_manager.create_task(task_copy)
        
        # Get statistics
        stats = await task_manager.get_task_statistics()
        
        assert 'total_tasks' in stats
        assert 'by_status' in stats
        assert 'by_priority' in stats
        assert stats['total_tasks'] >= 5

    @pytest.mark.asyncio
    async def test_task_validation(self, task_manager):
        """Test task data validation."""
        # Test with invalid task data
        invalid_task = {
            'title': '',  # Empty title should be invalid
            'priority': 'invalid_priority'  # Invalid priority
        }
        
        with pytest.raises(ValueError):
            await task_manager.create_task(invalid_task)

    @pytest.mark.asyncio
    async def test_concurrent_task_operations(self, task_manager, sample_task):
        """Test concurrent task operations."""
        task_data = sample_task.copy()
        del task_data['id']
        
        # Create multiple tasks concurrently
        async def create_task(index):
            task_copy = task_data.copy()
            task_copy['title'] = f"Concurrent Task {index}"
            return await task_manager.create_task(task_copy)
        
        # Create 5 tasks concurrently
        tasks = await asyncio.gather(*[
            create_task(i) for i in range(5)
        ])
        
        assert len(tasks) == 5
        for task in tasks:
            assert task is not None
            assert 'id' in task

    @pytest.mark.asyncio
    async def test_task_dependencies(self, task_manager, sample_task):
        """Test task dependency management."""
        task_data = sample_task.copy()
        del task_data['id']
        
        # Create parent task
        parent_task_data = task_data.copy()
        parent_task_data['title'] = "Parent Task"
        parent_task = await task_manager.create_task(parent_task_data)
        
        # Create child task with dependency
        child_task_data = task_data.copy()
        child_task_data['title'] = "Child Task"
        child_task_data['dependencies'] = [parent_task['id']]
        child_task = await task_manager.create_task(child_task_data)
        
        assert child_task['dependencies'] == [parent_task['id']]
        
        # Test dependency validation
        dependencies = await task_manager.get_task_dependencies(child_task['id'])
        assert parent_task['id'] in dependencies