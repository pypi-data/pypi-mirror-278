import sqlalchemy
from sqlmodel import SQLModel


def load_sql_models_metadata() -> sqlalchemy.MetaData:
    all_table_models: list[SQLModel] = [
        # BaseSQLModel,
        # User,
        # Project,
        # Objective,
        # KeyResult,
        # Requirement,
        # ScopedTask,
        # ScopedTaskStep,
        # TaskMessage,
        # TaskContext,
        # AiTask,
        # UserPrompt,
        # AiCompletion,
    ]
    print(f"{all_table_models=}")
    return SQLModel.metadata
