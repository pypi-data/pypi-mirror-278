import sqlalchemy
from sqlmodel import SQLModel

from ai_team_shared.models.ai_task_models import AiCompletion, AiTask
from ai_team_shared.models.base_models import BaseSQLModel
from ai_team_shared.models.context_models import TaskContext
from ai_team_shared.models.message_models import TaskMessage
from ai_team_shared.models.project_models import KeyResult, Objective, Project, Requirement, ScopedTask, ScopedTaskStep
from ai_team_shared.models.prompt_models import UserPrompt
from ai_team_shared.models.user_models import User


def load_sql_models_metadata() -> sqlalchemy.MetaData:
    all_table_models = [
        BaseSQLModel,
        User,
        Project,
        Objective,
        KeyResult,
        Requirement,
        ScopedTask,
        ScopedTaskStep,
        TaskMessage,
        TaskContext,
        AiTask,
        UserPrompt,
        AiCompletion,
    ]
    print(f"{all_table_models=}")
    return SQLModel.metadata
