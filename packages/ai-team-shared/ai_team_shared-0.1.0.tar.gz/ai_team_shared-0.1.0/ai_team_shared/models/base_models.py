from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

# Consider the correct usage of extend_existing for different environments
should_extend_existing = True


class BaseSQLModel(SQLModel):
    """
    BaseSQLModel is the base class for all SQL models
    - SQLModel is a thin wrapper around Pydantic and SQLAlchemy
    - Subclass of SQLModel can use any functionality from Pydantic and SQLAlchemy
    """
    __table_args__ = {"extend_existing": should_extend_existing}
    id: Optional[int] = Field(default=None, primary_key=True)
    # make this required in the future
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
