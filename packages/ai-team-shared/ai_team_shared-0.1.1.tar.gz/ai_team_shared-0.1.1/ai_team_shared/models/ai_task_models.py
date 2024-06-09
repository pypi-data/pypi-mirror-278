from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship

from .base_models import BaseSQLModel
from .context_models import TaskContext
from .message_models import TaskMessage
from .shared_enums import ModelNameLLM


class AiTaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class AiTask(BaseSQLModel, table=True):
    llm_model_name: ModelNameLLM
    prompt_text: str
    status: AiTaskStatus

    user_prompt_id: int = Field(foreign_key="userprompt.id")
    scoped_task_id: Optional[int] = Field(foreign_key="scopedtask.id")

    context: Optional[TaskContext] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
    messages: list[TaskMessage] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})


# Do not persist AiCompletion until: the use case is clear and AiTask table isn't enough
class AiCompletion(BaseSQLModel):
    success: bool
    text_output: Optional[str] = None
    json_output: Optional[dict] = None
    # add more fields for output display

    user_prompt_id: Optional[int] = None
