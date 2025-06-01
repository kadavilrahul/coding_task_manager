"""
Planner Agent for task planning and project roadmap generation.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from pathlib import Path
import json
from datetime import datetime, timedelta
from enum import Enum

from ..utils.file_utils import FileUtils
from ..utils.ai_utils import AIUtils


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class TaskStatus(Enum):
    """Task status options."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TaskType(Enum):
    """Types of tasks."""
    FEATURE = "feature"
    BUG_FIX = "bug_fix"
    REFACTOR = "refactor"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    RESEARCH = "research"
    SETUP = "setup"


class PlannerAgent:
    """Agent specialized in planning tasks and creating project roadmaps."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the planner agent."""
        self.config = config
        self.task_templates = self._load_task_templates()
        self.estimation_models = self._load_estimation_models()
    
    def _load_task_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load task templates for different types of work."""
        return {
            TaskType.FEATURE.value: {
                "phases": ["analysis", "design", "implementation", "testing", "documentation"],
                "base_effort": 8,  # hours
                "complexity_multiplier": 1.5
            },
            TaskType.BUG_FIX.value: {
                "phases": ["investigation", "fix", "testing", "verification"],
                "base_effort": 4,
                "complexity_multiplier": 1.2
            },
            TaskType.REFACTOR.value: {
                "phases": ["analysis", "planning", "refactoring", "testing", "documentation"],
                "base_effort": 12,
                "complexity_multiplier": 1.8
            },
            TaskType.DOCUMENTATION.value: {
                "phases": ["research", "writing", "review", "publishing"],
                "base_effort": 6,
                "complexity_multiplier": 1.0
            },
            TaskType.TESTING.value: {
                "phases": ["test_design", "implementation", "execution", "reporting"],
                "base_effort": 10,
                "complexity_multiplier": 1.3
            },
            TaskType.DEPLOYMENT.value: {
                "phases": ["preparation", "deployment", "verification", "monitoring"],
                "base_effort": 6,
                "complexity_multiplier": 1.4
            },
            TaskType.RESEARCH.value: {
                "phases": ["investigation", "analysis", "documentation", "presentation"],
                "base_effort": 16,
                "complexity_multiplier": 2.0
            },
            TaskType.SETUP.value: {
                "phases": ["planning", "installation", "configuration", "testing"],
                "base_effort": 8,
                "complexity_multiplier": 1.6
            }
        }
    
    def _load_estimation_models(self) -> Dict[str, Dict[str, float]]:
        """Load effort estimation models."""
        return {
            "complexity_factors": {
                "simple": 0.5,
                "moderate": 1.0,
                "complex": 2.0,
                "very_complex": 3.0
            },
            "technology_factors": {
                "familiar": 1.0,
                "somewhat_familiar": 1.3,
                "new": 1.8,
                "cutting_edge": 2.5
            },
            "team_factors": {
                "expert": 0.7,
                "experienced": 1.0,
                "intermediate": 1.4,
                "beginner": 2.0
            },
            "project_factors": {
                "greenfield": 1.0,
                "enhancement": 1.2,
                "legacy_integration": 1.8,
                "migration": 2.2
            }
        }
    
    def create_project_plan(self, project_info: Dict[str, Any], requirements: List[str]) -> Dict[str, Any]:
        """Create a comprehensive project plan."""
        plan = {
            "project_info": project_info,
            "created_at": datetime.now().isoformat(),
            "phases": [],
            "tasks": [],
            "milestones": [],
            "timeline": {},
            "resource_requirements": {},
            "risk_assessment": {},
            "success_criteria": []
        }
        
        try:
            # Analyze requirements and break them down
            analyzed_requirements = self._analyze_requirements(requirements)
            
            # Create project phases
            plan["phases"] = self._create_project_phases(project_info, analyzed_requirements)
            
            # Generate tasks for each phase
            plan["tasks"] = self._generate_tasks_from_phases(plan["phases"], analyzed_requirements)
            
            # Create milestones
            plan["milestones"] = self._create_milestones(plan["phases"], plan["tasks"])
            
            # Estimate timeline
            plan["timeline"] = self._estimate_timeline(plan["tasks"], plan["milestones"])
            
            # Assess resource requirements
            plan["resource_requirements"] = self._assess_resource_requirements(plan["tasks"])
            
            # Perform risk assessment
            plan["risk_assessment"] = self._assess_risks(project_info, plan["tasks"])
            
            # Define success criteria
            plan["success_criteria"] = self._define_success_criteria(project_info, requirements)
            
            return plan
        
        except Exception as e:
            return {
                "error": f"Failed to create project plan: {e}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _analyze_requirements(self, requirements: List[str]) -> Dict[str, Any]:
        """Analyze requirements to extract actionable items."""
        analysis = {
            "functional_requirements": [],
            "non_functional_requirements": [],
            "technical_requirements": [],
            "business_requirements": [],
            "complexity_assessment": {},
            "dependencies": [],
            "assumptions": []
        }
        
        for req in requirements:
            categorized_req = self._categorize_requirement(req)
            analysis[categorized_req["category"]].append(categorized_req)
        
        # Assess overall complexity
        analysis["complexity_assessment"] = self._assess_requirements_complexity(analysis)
        
        # Identify dependencies
        analysis["dependencies"] = self._identify_dependencies(analysis)
        
        return analysis
    
    def _categorize_requirement(self, requirement: str) -> Dict[str, Any]:
        """Categorize a single requirement."""
        req_lower = requirement.lower()
        
        # Keywords for different categories
        functional_keywords = ["user", "system", "function", "feature", "capability", "behavior"]
        non_functional_keywords = ["performance", "security", "usability", "reliability", "scalability"]
        technical_keywords = ["database", "api", "framework", "technology", "platform", "architecture"]
        business_keywords = ["business", "revenue", "cost", "roi", "market", "customer"]
        
        category = "functional_requirements"  # default
        
        if any(keyword in req_lower for keyword in non_functional_keywords):
            category = "non_functional_requirements"
        elif any(keyword in req_lower for keyword in technical_keywords):
            category = "technical_requirements"
        elif any(keyword in req_lower for keyword in business_keywords):
            category = "business_requirements"
        
        return {
            "text": requirement,
            "category": category,
            "complexity": self._estimate_requirement_complexity(requirement),
            "priority": self._estimate_requirement_priority(requirement),
            "effort_estimate": self._estimate_requirement_effort(requirement)
        }
    
    def _estimate_requirement_complexity(self, requirement: str) -> str:
        """Estimate the complexity of a requirement."""
        req_lower = requirement.lower()
        
        complex_indicators = ["integrate", "complex", "advanced", "multiple", "various", "comprehensive"]
        simple_indicators = ["simple", "basic", "straightforward", "minimal", "single"]
        
        if any(indicator in req_lower for indicator in complex_indicators):
            return "complex"
        elif any(indicator in req_lower for indicator in simple_indicators):
            return "simple"
        else:
            return "moderate"
    
    def _estimate_requirement_priority(self, requirement: str) -> TaskPriority:
        """Estimate the priority of a requirement."""
        req_lower = requirement.lower()
        
        high_priority_indicators = ["critical", "essential", "must", "required", "urgent"]
        low_priority_indicators = ["nice to have", "optional", "future", "enhancement", "could"]
        
        if any(indicator in req_lower for indicator in high_priority_indicators):
            return TaskPriority.HIGH
        elif any(indicator in req_lower for indicator in low_priority_indicators):
            return TaskPriority.LOW
        else:
            return TaskPriority.MEDIUM
    
    def _estimate_requirement_effort(self, requirement: str) -> int:
        """Estimate effort in hours for a requirement."""
        complexity = self._estimate_requirement_complexity(requirement)
        
        base_efforts = {
            "simple": 8,
            "moderate": 16,
            "complex": 32
        }
        
        return base_efforts.get(complexity, 16)
    
    def _assess_requirements_complexity(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall complexity of requirements."""
        total_requirements = sum(len(reqs) for reqs in analysis.values() if isinstance(reqs, list))
        
        complexity_counts = {}
        for req_list in [analysis["functional_requirements"], analysis["non_functional_requirements"], 
                        analysis["technical_requirements"], analysis["business_requirements"]]:
            for req in req_list:
                complexity = req.get("complexity", "moderate")
                complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1
        
        return {
            "total_requirements": total_requirements,
            "complexity_distribution": complexity_counts,
            "overall_complexity": self._calculate_overall_complexity(complexity_counts),
            "estimated_total_effort": sum(req.get("effort_estimate", 0) 
                                        for req_list in [analysis["functional_requirements"], 
                                                       analysis["non_functional_requirements"],
                                                       analysis["technical_requirements"], 
                                                       analysis["business_requirements"]]
                                        for req in req_list)
        }
    
    def _calculate_overall_complexity(self, complexity_counts: Dict[str, int]) -> str:
        """Calculate overall project complexity."""
        total = sum(complexity_counts.values())
        if total == 0:
            return "simple"
        
        complex_ratio = complexity_counts.get("complex", 0) / total
        
        if complex_ratio > 0.5:
            return "very_complex"
        elif complex_ratio > 0.3:
            return "complex"
        elif complexity_counts.get("moderate", 0) / total > 0.6:
            return "moderate"
        else:
            return "simple"
    
    def _identify_dependencies(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify dependencies between requirements."""
        dependencies = []
        
        # This is a simplified dependency detection
        # In a real implementation, this would use more sophisticated analysis
        
        all_requirements = []
        for req_list in [analysis["functional_requirements"], analysis["non_functional_requirements"],
                        analysis["technical_requirements"], analysis["business_requirements"]]:
            all_requirements.extend(req_list)
        
        # Look for common dependency patterns
        for i, req1 in enumerate(all_requirements):
            for j, req2 in enumerate(all_requirements):
                if i != j:
                    dependency = self._check_dependency(req1, req2)
                    if dependency:
                        dependencies.append(dependency)
        
        return dependencies
    
    def _check_dependency(self, req1: Dict[str, Any], req2: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check if there's a dependency between two requirements."""
        text1 = req1["text"].lower()
        text2 = req2["text"].lower()
        
        # Simple keyword-based dependency detection
        dependency_patterns = [
            ("database", "api"),
            ("authentication", "user"),
            ("setup", "configuration"),
            ("framework", "implementation")
        ]
        
        for pattern1, pattern2 in dependency_patterns:
            if pattern1 in text1 and pattern2 in text2:
                return {
                    "prerequisite": req1["text"],
                    "dependent": req2["text"],
                    "type": "technical",
                    "strength": "medium"
                }
        
        return None
    
    def _create_project_phases(self, project_info: Dict[str, Any], 
                             analyzed_requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create project phases based on project type and requirements."""
        project_type = project_info.get("project_type", "unknown")
        complexity = analyzed_requirements["complexity_assessment"]["overall_complexity"]
        
        # Standard phases for different project types
        phase_templates = {
            "web_application": [
                {"name": "Planning & Analysis", "duration_weeks": 2},
                {"name": "Design & Architecture", "duration_weeks": 3},
                {"name": "Backend Development", "duration_weeks": 6},
                {"name": "Frontend Development", "duration_weeks": 5},
                {"name": "Integration & Testing", "duration_weeks": 3},
                {"name": "Deployment & Launch", "duration_weeks": 2}
            ],
            "mobile_app": [
                {"name": "Planning & Research", "duration_weeks": 2},
                {"name": "UI/UX Design", "duration_weeks": 3},
                {"name": "Core Development", "duration_weeks": 8},
                {"name": "Testing & QA", "duration_weeks": 3},
                {"name": "App Store Submission", "duration_weeks": 2}
            ],
            "api": [
                {"name": "API Design", "duration_weeks": 2},
                {"name": "Core Implementation", "duration_weeks": 4},
                {"name": "Testing & Documentation", "duration_weeks": 2},
                {"name": "Deployment & Monitoring", "duration_weeks": 1}
            ],
            "data_analysis": [
                {"name": "Data Collection & Cleaning", "duration_weeks": 3},
                {"name": "Exploratory Analysis", "duration_weeks": 2},
                {"name": "Model Development", "duration_weeks": 4},
                {"name": "Validation & Testing", "duration_weeks": 2},
                {"name": "Reporting & Presentation", "duration_weeks": 1}
            ],
            "default": [
                {"name": "Planning", "duration_weeks": 1},
                {"name": "Implementation", "duration_weeks": 4},
                {"name": "Testing", "duration_weeks": 2},
                {"name": "Deployment", "duration_weeks": 1}
            ]
        }
        
        phases = phase_templates.get(project_type, phase_templates["default"])
        
        # Adjust durations based on complexity
        complexity_multipliers = {
            "simple": 0.7,
            "moderate": 1.0,
            "complex": 1.5,
            "very_complex": 2.0
        }
        
        multiplier = complexity_multipliers.get(complexity, 1.0)
        
        for phase in phases:
            phase["duration_weeks"] = max(1, int(phase["duration_weeks"] * multiplier))
            phase["status"] = TaskStatus.PENDING.value
            phase["tasks"] = []
        
        return phases
    
    def _generate_tasks_from_phases(self, phases: List[Dict[str, Any]], 
                                  analyzed_requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific tasks for each phase."""
        tasks = []
        task_id = 1
        
        for phase_idx, phase in enumerate(phases):
            phase_tasks = self._generate_phase_tasks(phase, analyzed_requirements, task_id)
            tasks.extend(phase_tasks)
            task_id += len(phase_tasks)
            
            # Update phase with task IDs
            phase["tasks"] = [task["id"] for task in phase_tasks]
        
        return tasks
    
    def _generate_phase_tasks(self, phase: Dict[str, Any], 
                            analyzed_requirements: Dict[str, Any], 
                            start_id: int) -> List[Dict[str, Any]]:
        """Generate tasks for a specific phase."""
        phase_name = phase["name"].lower()
        tasks = []
        task_id = start_id
        
        # Task templates for different phases
        if "planning" in phase_name or "analysis" in phase_name:
            task_templates = [
                {"name": "Requirements Analysis", "type": TaskType.RESEARCH, "effort_hours": 16},
                {"name": "Technical Architecture Design", "type": TaskType.DESIGN, "effort_hours": 12},
                {"name": "Project Setup", "type": TaskType.SETUP, "effort_hours": 8},
                {"name": "Development Environment Setup", "type": TaskType.SETUP, "effort_hours": 6}
            ]
        elif "design" in phase_name:
            task_templates = [
                {"name": "System Architecture Design", "type": TaskType.DESIGN, "effort_hours": 20},
                {"name": "Database Schema Design", "type": TaskType.DESIGN, "effort_hours": 12},
                {"name": "API Design", "type": TaskType.DESIGN, "effort_hours": 16},
                {"name": "UI/UX Mockups", "type": TaskType.DESIGN, "effort_hours": 24}
            ]
        elif "development" in phase_name or "implementation" in phase_name:
            task_templates = [
                {"name": "Core Feature Implementation", "type": TaskType.FEATURE, "effort_hours": 40},
                {"name": "Database Implementation", "type": TaskType.FEATURE, "effort_hours": 20},
                {"name": "API Implementation", "type": TaskType.FEATURE, "effort_hours": 30},
                {"name": "Frontend Implementation", "type": TaskType.FEATURE, "effort_hours": 35}
            ]
        elif "testing" in phase_name:
            task_templates = [
                {"name": "Unit Testing", "type": TaskType.TESTING, "effort_hours": 20},
                {"name": "Integration Testing", "type": TaskType.TESTING, "effort_hours": 16},
                {"name": "User Acceptance Testing", "type": TaskType.TESTING, "effort_hours": 12},
                {"name": "Performance Testing", "type": TaskType.TESTING, "effort_hours": 8}
            ]
        elif "deployment" in phase_name:
            task_templates = [
                {"name": "Production Environment Setup", "type": TaskType.DEPLOYMENT, "effort_hours": 12},
                {"name": "Application Deployment", "type": TaskType.DEPLOYMENT, "effort_hours": 8},
                {"name": "Monitoring Setup", "type": TaskType.DEPLOYMENT, "effort_hours": 6},
                {"name": "Documentation", "type": TaskType.DOCUMENTATION, "effort_hours": 10}
            ]
        else:
            task_templates = [
                {"name": f"{phase['name']} Task", "type": TaskType.FEATURE, "effort_hours": 16}
            ]
        
        for template in task_templates:
            task = {
                "id": task_id,
                "name": template["name"],
                "description": f"Task for {phase['name']} phase",
                "type": template["type"].value,
                "status": TaskStatus.PENDING.value,
                "priority": TaskPriority.MEDIUM.value,
                "effort_hours": template["effort_hours"],
                "phase": phase["name"],
                "dependencies": [],
                "assigned_to": None,
                "created_at": datetime.now().isoformat(),
                "due_date": None,
                "completion_percentage": 0,
                "notes": []
            }
            
            tasks.append(task)
            task_id += 1
        
        return tasks
    
    def _create_milestones(self, phases: List[Dict[str, Any]], 
                          tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create project milestones."""
        milestones = []
        milestone_id = 1
        
        for phase in phases:
            milestone = {
                "id": milestone_id,
                "name": f"{phase['name']} Complete",
                "description": f"Completion of {phase['name']} phase",
                "phase": phase["name"],
                "criteria": self._define_milestone_criteria(phase, tasks),
                "target_date": None,  # Will be set in timeline estimation
                "status": TaskStatus.PENDING.value,
                "dependencies": []
            }
            
            milestones.append(milestone)
            milestone_id += 1
        
        return milestones
    
    def _define_milestone_criteria(self, phase: Dict[str, Any], 
                                 tasks: List[Dict[str, Any]]) -> List[str]:
        """Define criteria for milestone completion."""
        phase_tasks = [task for task in tasks if task["phase"] == phase["name"]]
        
        criteria = [
            f"All {len(phase_tasks)} tasks in {phase['name']} phase completed",
            "Quality review passed",
            "Documentation updated"
        ]
        
        # Add phase-specific criteria
        phase_name = phase["name"].lower()
        
        if "design" in phase_name:
            criteria.extend([
                "Design documents approved",
                "Architecture review completed"
            ])
        elif "development" in phase_name:
            criteria.extend([
                "Code review completed",
                "Unit tests passing"
            ])
        elif "testing" in phase_name:
            criteria.extend([
                "All test cases executed",
                "Bug fixes implemented",
                "Test report generated"
            ])
        elif "deployment" in phase_name:
            criteria.extend([
                "Production deployment successful",
                "Monitoring systems active",
                "User training completed"
            ])
        
        return criteria
    
    def _estimate_timeline(self, tasks: List[Dict[str, Any]], 
                          milestones: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Estimate project timeline."""
        timeline = {
            "start_date": datetime.now().date().isoformat(),
            "estimated_end_date": None,
            "total_effort_hours": 0,
            "total_duration_weeks": 0,
            "phase_schedule": [],
            "critical_path": []
        }
        
        # Calculate total effort
        timeline["total_effort_hours"] = sum(task["effort_hours"] for task in tasks)
        
        # Estimate duration assuming 40 hours per week
        hours_per_week = 40
        timeline["total_duration_weeks"] = max(1, timeline["total_effort_hours"] // hours_per_week)
        
        # Calculate end date
        start_date = datetime.now().date()
        end_date = start_date + timedelta(weeks=timeline["total_duration_weeks"])
        timeline["estimated_end_date"] = end_date.isoformat()
        
        # Create phase schedule
        current_date = start_date
        for milestone in milestones:
            phase_tasks = [task for task in tasks if task["phase"] == milestone["phase"]]
            phase_effort = sum(task["effort_hours"] for task in phase_tasks)
            phase_weeks = max(1, phase_effort // hours_per_week)
            
            phase_end_date = current_date + timedelta(weeks=phase_weeks)
            
            timeline["phase_schedule"].append({
                "phase": milestone["phase"],
                "start_date": current_date.isoformat(),
                "end_date": phase_end_date.isoformat(),
                "duration_weeks": phase_weeks,
                "effort_hours": phase_effort
            })
            
            milestone["target_date"] = phase_end_date.isoformat()
            current_date = phase_end_date
        
        # Identify critical path (simplified)
        timeline["critical_path"] = self._identify_critical_path(tasks)
        
        return timeline
    
    def _identify_critical_path(self, tasks: List[Dict[str, Any]]) -> List[int]:
        """Identify the critical path through tasks."""
        # Simplified critical path identification
        # In a real implementation, this would use proper CPM algorithms
        
        # For now, just return the longest sequence of dependent tasks
        critical_tasks = []
        
        # Sort tasks by effort (descending) as a simple heuristic
        sorted_tasks = sorted(tasks, key=lambda x: x["effort_hours"], reverse=True)
        
        # Take the top 30% of tasks by effort as critical
        critical_count = max(1, len(sorted_tasks) // 3)
        critical_tasks = [task["id"] for task in sorted_tasks[:critical_count]]
        
        return critical_tasks
    
    def _assess_resource_requirements(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess resource requirements for the project."""
        requirements = {
            "team_size": 0,
            "skill_requirements": {},
            "tools_and_technologies": [],
            "budget_estimate": {},
            "external_dependencies": []
        }
        
        # Estimate team size based on total effort
        total_effort = sum(task["effort_hours"] for task in tasks)
        project_duration_weeks = max(1, total_effort // 40)  # Assuming 40 hours/week
        
        # Aim for reasonable project duration (12-24 weeks)
        if project_duration_weeks > 24:
            requirements["team_size"] = max(2, total_effort // (24 * 40))
        else:
            requirements["team_size"] = 1
        
        # Identify skill requirements based on task types
        task_types = [task["type"] for task in tasks]
        type_counts = {}
        for task_type in task_types:
            type_counts[task_type] = type_counts.get(task_type, 0) + 1
        
        # Map task types to skills
        skill_mapping = {
            TaskType.FEATURE.value: ["software_development", "programming"],
            TaskType.BUG_FIX.value: ["debugging", "problem_solving"],
            TaskType.REFACTOR.value: ["code_architecture", "software_design"],
            TaskType.DOCUMENTATION.value: ["technical_writing", "documentation"],
            TaskType.TESTING.value: ["quality_assurance", "testing"],
            TaskType.DEPLOYMENT.value: ["devops", "system_administration"],
            TaskType.RESEARCH.value: ["research", "analysis"],
            TaskType.SETUP.value: ["system_configuration", "setup"]
        }
        
        for task_type, count in type_counts.items():
            skills = skill_mapping.get(task_type, ["general"])
            for skill in skills:
                requirements["skill_requirements"][skill] = requirements["skill_requirements"].get(skill, 0) + count
        
        # Estimate budget (simplified)
        hourly_rate = 75  # Average hourly rate
        requirements["budget_estimate"] = {
            "development_cost": total_effort * hourly_rate,
            "tools_and_licenses": 5000,  # Estimated
            "infrastructure": 2000,  # Estimated
            "contingency": (total_effort * hourly_rate) * 0.2  # 20% contingency
        }
        
        total_budget = sum(requirements["budget_estimate"].values())
        requirements["budget_estimate"]["total"] = total_budget
        
        return requirements
    
    def _assess_risks(self, project_info: Dict[str, Any], 
                     tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess project risks."""
        risks = {
            "technical_risks": [],
            "schedule_risks": [],
            "resource_risks": [],
            "business_risks": [],
            "mitigation_strategies": {}
        }
        
        # Technical risks
        tech_stack = project_info.get("tech_stack", [])
        if len(tech_stack) > 5:
            risks["technical_risks"].append({
                "risk": "Complex technology stack",
                "probability": "medium",
                "impact": "high",
                "description": "Multiple technologies increase integration complexity"
            })
        
        # Schedule risks
        total_effort = sum(task["effort_hours"] for task in tasks)
        if total_effort > 1000:
            risks["schedule_risks"].append({
                "risk": "Large project scope",
                "probability": "high",
                "impact": "high",
                "description": "Large projects are prone to schedule overruns"
            })
        
        # Resource risks
        complex_tasks = [task for task in tasks if task["effort_hours"] > 40]
        if len(complex_tasks) > len(tasks) * 0.3:
            risks["resource_risks"].append({
                "risk": "High skill requirements",
                "probability": "medium",
                "impact": "medium",
                "description": "Many complex tasks require experienced developers"
            })
        
        # Generate mitigation strategies
        risks["mitigation_strategies"] = self._generate_mitigation_strategies(risks)
        
        return risks
    
    def _generate_mitigation_strategies(self, risks: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate mitigation strategies for identified risks."""
        strategies = {
            "technical": [
                "Conduct proof-of-concept for new technologies",
                "Implement comprehensive testing strategy",
                "Plan for regular architecture reviews",
                "Maintain technical documentation"
            ],
            "schedule": [
                "Break down large tasks into smaller ones",
                "Add buffer time for complex tasks",
                "Implement regular progress reviews",
                "Plan for scope adjustments if needed"
            ],
            "resource": [
                "Identify skill gaps early",
                "Plan for training or hiring",
                "Consider external consultants for specialized tasks",
                "Implement knowledge sharing practices"
            ],
            "business": [
                "Maintain regular stakeholder communication",
                "Document and validate requirements",
                "Plan for change management",
                "Establish clear success criteria"
            ]
        }
        
        return strategies
    
    def _define_success_criteria(self, project_info: Dict[str, Any], 
                               requirements: List[str]) -> List[Dict[str, Any]]:
        """Define success criteria for the project."""
        criteria = [
            {
                "category": "functional",
                "criterion": "All functional requirements implemented",
                "measurement": "100% of features working as specified",
                "priority": "high"
            },
            {
                "category": "quality",
                "criterion": "Code quality standards met",
                "measurement": "Code review approval and test coverage > 80%",
                "priority": "high"
            },
            {
                "category": "performance",
                "criterion": "Performance requirements met",
                "measurement": "Response times within specified limits",
                "priority": "medium"
            },
            {
                "category": "schedule",
                "criterion": "Project delivered on time",
                "measurement": "Delivery within planned timeline",
                "priority": "medium"
            },
            {
                "category": "budget",
                "criterion": "Project within budget",
                "measurement": "Costs within approved budget",
                "priority": "high"
            }
        ]
        
        # Add project-specific criteria
        project_type = project_info.get("project_type", "")
        
        if "web" in project_type:
            criteria.append({
                "category": "usability",
                "criterion": "User experience standards met",
                "measurement": "User testing feedback positive",
                "priority": "medium"
            })
        
        if "api" in project_type:
            criteria.append({
                "category": "documentation",
                "criterion": "API documentation complete",
                "measurement": "All endpoints documented with examples",
                "priority": "high"
            })
        
        return criteria
    
    def update_task_status(self, task_id: int, new_status: TaskStatus, 
                          completion_percentage: Optional[int] = None,
                          notes: Optional[str] = None) -> Dict[str, Any]:
        """Update the status of a specific task."""
        update_result = {
            "task_id": task_id,
            "old_status": None,
            "new_status": new_status.value,
            "updated_at": datetime.now().isoformat(),
            "success": False,
            "message": ""
        }
        
        # In a real implementation, this would update the task in a database
        # For now, we'll just return the update information
        
        update_result["success"] = True
        update_result["message"] = f"Task {task_id} status updated to {new_status.value}"
        
        if completion_percentage is not None:
            update_result["completion_percentage"] = completion_percentage
        
        if notes:
            update_result["notes_added"] = notes
        
        return update_result
    
    def get_project_status(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Get current project status based on task completion."""
        status = {
            "overall_progress": 0,
            "phase_progress": {},
            "completed_tasks": 0,
            "total_tasks": len(plan.get("tasks", [])),
            "overdue_tasks": 0,
            "blocked_tasks": 0,
            "next_milestones": [],
            "critical_issues": []
        }
        
        tasks = plan.get("tasks", [])
        
        # Calculate overall progress
        if tasks:
            completed_tasks = [task for task in tasks if task.get("status") == TaskStatus.COMPLETED.value]
            status["completed_tasks"] = len(completed_tasks)
            status["overall_progress"] = (len(completed_tasks) / len(tasks)) * 100
        
        # Calculate phase progress
        phases = plan.get("phases", [])
        for phase in phases:
            phase_tasks = [task for task in tasks if task.get("phase") == phase["name"]]
            if phase_tasks:
                completed_phase_tasks = [task for task in phase_tasks 
                                       if task.get("status") == TaskStatus.COMPLETED.value]
                phase_progress = (len(completed_phase_tasks) / len(phase_tasks)) * 100
                status["phase_progress"][phase["name"]] = phase_progress
        
        # Count blocked tasks
        status["blocked_tasks"] = len([task for task in tasks 
                                     if task.get("status") == TaskStatus.BLOCKED.value])
        
        # Identify next milestones
        milestones = plan.get("milestones", [])
        pending_milestones = [milestone for milestone in milestones 
                            if milestone.get("status") == TaskStatus.PENDING.value]
        status["next_milestones"] = pending_milestones[:3]  # Next 3 milestones
        
        return status
    
    def generate_plan_summary(self, plan: Dict[str, Any]) -> str:
        """Generate a human-readable summary of the project plan."""
        summary_parts = [
            f"Project Plan Summary:",
            f"- Total Tasks: {len(plan.get('tasks', []))}",
            f"- Phases: {len(plan.get('phases', []))}",
            f"- Estimated Duration: {plan.get('timeline', {}).get('total_duration_weeks', 0)} weeks",
            f"- Total Effort: {plan.get('timeline', {}).get('total_effort_hours', 0)} hours",
            f"- Team Size: {plan.get('resource_requirements', {}).get('team_size', 1)}",
            f"- Budget Estimate: ${plan.get('resource_requirements', {}).get('budget_estimate', {}).get('total', 0):,.0f}"
        ]
        
        # Add phase information
        phases = plan.get("phases", [])
        if phases:
            summary_parts.append("\nPhases:")
            for phase in phases:
                summary_parts.append(f"  - {phase['name']}: {phase.get('duration_weeks', 0)} weeks")
        
        # Add risk summary
        risks = plan.get("risk_assessment", {})
        total_risks = sum(len(risk_list) for risk_list in risks.values() if isinstance(risk_list, list))
        if total_risks > 0:
            summary_parts.append(f"\nIdentified Risks: {total_risks}")
        
        return '\n'.join(summary_parts)