from typing import Optional

import sqlalchemy
from pydantic import BaseModel
from sqlmodel import Field

from .base_models import BaseSQLModel
from .shared_enums import ModelNameLLM, TaskType


class UserPrompt(BaseSQLModel, table=True):
    prompt_text: str
    response_class_name: Optional[str] = None

    # This should support module notation
    input_files: list[str] = Field(sa_type=sqlalchemy.JSON)
    output_files: list[str] = Field(sa_type=sqlalchemy.JSON)
    # Support data change later

    # LLM Model Config
    llm_model_name: ModelNameLLM
    # add Temperature, etc

    # add user_id; consider required vs optional, creation timing and place
    # user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    scoped_task_id: Optional[int] = Field(default=None, foreign_key="scopedtask.id")


class PromptTemplate(BaseModel):
    task_type: TaskType
    scope: str
    response_class_name: str
    general_instruction: str
    scoped_instruction: str
    input_files: list[str]
    output_files: list[str]


class PromptTemplateSimple(BaseModel):
    response_class_name: str
    task_description: str
    extra_instructions: list[str]
    input_files: list[str]
