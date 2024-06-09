from enum import Enum
from typing import Optional

from .base_models import BaseSQLModel


# TODO: use this to pass test; run migration after we are ready to persist the changes in DB

class FileChangeType(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class FileChange(BaseSQLModel):
    change_type: FileChangeType
    file_uri: str
    file_content: Optional[str] = None


class AiFileChanges(BaseSQLModel):
    summary: str
    file_changes: list[FileChange]


# TODO: consider the association of AiFileChanges, Testing and AiTask better; models below are just a draft


class FileChangeStatus(str, Enum):
    PENDING = "PENDING"
    APPLIED = "APPLIED"
    TESTED = "TESTED"
    REVERTED = "REVERTED"
    COMMITTED = "COMMITTED"


class FileChangesTest(BaseSQLModel):
    test_type: str
    test_passed: bool
    failure_message: Optional[str] = None
    test_cases: Optional[dict] = None


class FileChangesResult(BaseSQLModel):
    status: FileChangeStatus
    summary: str
    file_changes: list[FileChange]
    tests: list[FileChangesTest]
    # ai_file_changes_id: Optional[int] = Field(default=None, foreign_key="aifilechanges.id")
    # ai_task_id: Optional[int] = Field(default=None, foreign_key="aitask.id")
