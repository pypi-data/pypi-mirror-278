from typing import Optional

import sqlalchemy
from pydantic import BaseModel
from sqlmodel import Field

from .base_models import BaseSQLModel
from .project_models import KeyResult, Objective, Project, Requirement, ScopedTask


class TaskResponseFormat(BaseModel):
    data_model_class: str
    data_model_schema: Optional[dict] = None
    data_model_example: Optional[dict] = None


class ProjectContext(BaseModel):
    project: Project
    objective: Objective
    key_result: KeyResult
    requirement: Requirement
    scoped_task: ScopedTask


class FileContext(BaseModel):
    file_uri: str
    file_content: Optional[str] = None


class TaskContext(BaseSQLModel, table=True):
    response_format: Optional[TaskResponseFormat] = Field(default=None, sa_type=sqlalchemy.JSON)
    project_context: Optional[ProjectContext] = Field(default=None, sa_type=sqlalchemy.JSON)
    input_files: list[FileContext] = Field(sa_type=sqlalchemy.JSON)
    output_files: list[str] = Field(sa_type=sqlalchemy.JSON)

    ai_task_id: Optional[int] = Field(default=None, foreign_key="aitask.id")
    scoped_task_id: Optional[int] = Field(default=None, foreign_key="scopedtask.id")
