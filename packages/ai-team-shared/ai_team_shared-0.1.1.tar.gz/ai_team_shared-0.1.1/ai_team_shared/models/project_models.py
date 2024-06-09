from datetime import datetime
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel
from sqlmodel import Field

from .base_models import BaseSQLModel
from .shared_enums import TaskType

"""
Fix this if possible: All class have the same mypy error: 
Metaclass conflict: 
the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases  [misc]
"""


class StatusType(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    # ERROR = "ERROR"


class AssigneeType(str, Enum):
    CODER = "CODER"
    CTO = "CTO"
    CEO = "CEO"
    COO = "COO"


class NecessityType(str, Enum):
    """Must/Should/Could/Won't Have"""
    MUST = "MUST"
    SHOULD = "SHOULD"
    COULD = "COULD"
    WONT = "WONT"


class PriorityType(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class BaseProjectModel(BaseSQLModel):
    description: str
    status: StatusType
    name: str

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    # Support these fields in the future
    # estimated_duration: Optional[str]
    # deadline: Optional[datetime]

    # TODO: add validator for start_date and end_date and status


class Project(BaseProjectModel, table=True):
    pass


class Objective(BaseProjectModel, table=True):
    project_id: int = Field(foreign_key="project.id")


class KeyResult(BaseProjectModel, table=True):
    objective_id: int = Field(foreign_key="objective.id")


class Requirement(BaseProjectModel, table=True):
    key_result_id: int = Field(foreign_key="keyresult.id")
    necessity: NecessityType


class ScopedTask(BaseProjectModel, table=True):
    requirement_id: int = Field(foreign_key="requirement.id")
    assignee: Optional[AssigneeType] = None
    priority: Optional[PriorityType] = None
    task_type: Optional[TaskType] = TaskType.UNDEFINED

    # Additional fields to provide more information
    # estimated_duration: Optional[str]
    # difficulty: Optional[str]

    # This can be used to link the task to Gitlab MR
    # merge_request_id: Optional[str] = None


class ScopedTaskStep(BaseSQLModel, table=True):
    task_id: int = Field(foreign_key="scopedtask.id")
    action: str
    status: StatusType
    expected_result: Optional[str] = None
    # consider adding execution_log here


# Roadmap are pydantic models and not SQL models. It uses files to store and directly edit.
# It can be converted to SQL model if needed.

class RoadmapMilestone(BaseModel):
    title: str
    description: str
    date: datetime
    type: Literal['HISTORICAL', 'FUTURE']
    category: Literal['KEY-METRICS', 'TRADING-ENGINE', 'ML-MODEL', 'INFRASTRUCTURE', 'AI-TEAM', 'OPERATIONS', 'HIRING']


class Roadmap(BaseModel):
    name: str
    description: str
    milestones: list[RoadmapMilestone] = []

    @property
    def historical_milestones(self) -> list[RoadmapMilestone]:
        return [m for m in self.milestones if m.type == 'HISTORICAL']

    @property
    def future_milestones(self) -> list[RoadmapMilestone]:
        return [m for m in self.milestones if m.type == 'FUTURE']


# These are view models which are not stored in the database. They are used to specify AI response and their display.

class OKR(BaseModel):
    objective: Objective
    key_results: list[KeyResult]


class KeyResultRequirements(BaseModel):
    key_result: KeyResult
    requirements: list[Requirement]


class ScopedTaskStepList(BaseModel):
    task_id: int
    steps: list[ScopedTaskStep]
