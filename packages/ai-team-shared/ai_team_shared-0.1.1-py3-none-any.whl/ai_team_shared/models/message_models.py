from enum import Enum
from typing import Optional

from sqlmodel import Field

from .base_models import BaseSQLModel


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class TaskMessage(BaseSQLModel, table=True):
    content: str
    role: MessageRole

    ai_task_id: Optional[int] = Field(default=None, foreign_key="aitask.id")

# TODO: move message models:
#  - consider how to consolidate StandardMessage and TaskMessage
#  - consider using a single message in response

# class StandardMessage(BaseModel):
#     content: str
#     role: Literal["user", "assistant"]
#
#
# class CreateMessageRequest(BaseModel):
#     model: ModelNameLLM
#     messages: list[StandardMessage]
#     json_mode: bool = False
#     system_message: Optional[str] = None
#
#
# class CreateMessageResponse(BaseModel):
#     messages: list[StandardMessage]
#     json_dict: Optional[dict] = None
